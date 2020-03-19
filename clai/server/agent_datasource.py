#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

# pylint: disable=ungrouped-imports
import configparser
import importlib
import inspect
import os
import pkgutil as pkg
from typing import List, Optional, Dict

import clai.server.plugins
from clai.datasource.config_storage import config_storage as config, ConfigStorage
from clai.datasource.model.plugin_config import PluginConfig
from clai.server.agent import Agent, ClaiIdentity
from clai.server.agent_datasource_executor import thread_agent_datasource_executor as agent_datasource_executor
from clai.server.command_runner.agent_descriptor import AgentDescriptor
from clai.server.logger import current_logger as logger


class AgentDatasource:

    def __init__(self, config_storage: ConfigStorage = config):
        self.__selected_plugin: Dict[str, Optional[List[pkg.ModuleInfo]]] = {}
        self.__plugins: Dict[str, Agent] = {}
        self.num_workers = 4
        self.config_storage = config_storage
        self.current_orchestrator = None

    @staticmethod
    def get_path():
        return clai.server.plugins.__path__

    def preload_plugins(self):
        all_descriptors = self.all_plugins()
        installed_agents = list(filter(lambda value: value.installed, all_descriptors))
        for descriptor in installed_agents:
            self.start_agent(descriptor)

        logger.info("finish init")

    def start_agent(self, descriptor):
        agent_datasource_executor.execute(self.load_agent, descriptor.pkg_name)

    def load_agent(self, name: str):
        try:
            plugin = importlib.import_module(
                f'clai.server.plugins.{name}.{name}', package=name)

            importlib.invalidate_caches()
            plugin = importlib.reload(plugin)

            for _, class_member in inspect.getmembers(plugin, inspect.isclass):
                if issubclass(class_member, Agent) and (class_member is not Agent):
                    member = class_member()
                    if not member:
                        member = ClaiIdentity()
                    self.__plugins[name] = member
                    member.init_agent()
                    member.ready = True
                    logger.info(f"{name} is ready")
        # pylint: disable=broad-except
        except Exception as ex:
            logger.info(f'load agent exception: {ex}')

    def get_instances(self, user_name: str, agent_to_select: str = None) -> List[Agent]:
        select_plugins_by_user = self.__get_selected_by_user(user_name)

        if select_plugins_by_user is None:
            self.init_plugin_config(user_name)
            select_plugins_by_user = self.__get_selected_by_user(user_name)

        if agent_to_select:
            agent_descriptor_selected = self.get_agent_descriptor(agent_to_select)

            if agent_descriptor_selected is None:
                return [ClaiIdentity()]

            select_plugins_by_user = list(
                filter(lambda value: value.name == agent_descriptor_selected.pkg_name,
                       select_plugins_by_user))

        if agent_to_select:
            agent_descriptor_selected = self.get_agent_descriptor(agent_to_select)
            if agent_descriptor_selected is None:
                return [ClaiIdentity()]

            select_plugins_by_user = list(
                filter(lambda value: value.name == agent_descriptor_selected.pkg_name,
                       select_plugins_by_user))

        agents = []
        for select_plugin_by_user in select_plugins_by_user:
            if select_plugin_by_user.name in self.__plugins:
                agent = self.__plugins[select_plugin_by_user.name]
                if agent.ready:
                    agents.append(agent)

        if not agents:
            agents.append(ClaiIdentity())

        return agents

    @staticmethod
    def load_descriptors(path, name) -> AgentDescriptor:
        file_path = os.path.join(path, "manifest.properties")
        if os.path.exists(file_path):
            config_parser = configparser.ConfigParser()
            config_parser.read(file_path)

            default = False
            if config_parser.has_option('DEFAULT', 'default'):
                default = config_parser.getboolean('DEFAULT', 'default')

            exclude = []
            if config_parser.has_option('DEFAULT', 'exclude'):
                exclude = config_parser.get('DEFAULT', 'exclude').lower().split()

            return AgentDescriptor(
                pkg_name=name,
                name=config_parser['DEFAULT']['name'],
                description=config_parser['DEFAULT']['description'],
                exclude=exclude,
                default=default
            )

        return AgentDescriptor(
            pkg_name=name,
            name=name)

    def get_report_enable(self) -> bool:
        plugins_config = self.config_storage.read_config(None)
        return plugins_config.report_enable

    def mark_report_enable(self, report_enable):
        plugins_config = self.config_storage.read_config(None)
        plugins_config.report_enable = report_enable
        self.config_storage.store_config(plugins_config, None)

    def mark_plugins_as_installed(self, name_plugin: str, user_name: Optional[str]):
        plugins_config = self.config_storage.read_config(user_name)

        if name_plugin not in plugins_config.installed:
            plugins_config.installed.append(name_plugin)
        self.config_storage.store_config(plugins_config, user_name)

    @staticmethod
    def filter_by_platform(agent_descriptors: List[AgentDescriptor]) -> List[AgentDescriptor]:
        os_name = os.uname().sysname.lower()
        return list(filter(lambda agent: os_name not in agent.exclude, agent_descriptors))

    def all_plugins(self) -> List[AgentDescriptor]:
        agent_descriptors = list(
            self.load_descriptors(os.path.join(importer.path, name), name)
            for importer, name, _
            in pkg.iter_modules(self.get_path()))

        agent_descriptors = self.filter_by_platform(agent_descriptors)

        plugins_installed = self.config_storage.load_installed()

        for agent_descriptor in agent_descriptors:
            agent_descriptor.installed = agent_descriptor.name in plugins_installed

        logger.info(f"agents runned: {self.__plugins}")
        for agent_descriptor in agent_descriptors:
            if agent_descriptor.pkg_name in self.__plugins:
                logger.info(f"{agent_descriptor.pkg_name} is {self.__plugins[agent_descriptor.pkg_name].ready}")
                agent_descriptor.ready = self.__plugins[agent_descriptor.pkg_name].ready
            else:
                logger.info(f"{agent_descriptor.pkg_name} not iniciate.")
                agent_descriptor.ready = False

        return agent_descriptors

    def get_current_orchestrator(self) -> str:
        if not self.current_orchestrator:
            plugin_config = self.config_storage.read_config()
            self.current_orchestrator = plugin_config.default_orchestrator
            plugin_config.orchestrator = self.current_orchestrator
            self.config_storage.store_config(plugin_config)

        return self.current_orchestrator

    def select_orchestrator(self, orchestrator_name: str):
        plugin_config = self.config_storage.read_config()
        self.current_orchestrator = orchestrator_name
        plugin_config.orchestrator = self.current_orchestrator
        self.config_storage.store_config(config)

    def get_current_plugin_name(self, user_name: str) -> List[str]:
        selected_plugin = self.__get_selected_by_user(user_name)
        if selected_plugin is None:
            self.init_plugin_config(user_name)
            selected_plugin = self.__get_selected_by_user(user_name)
        if not selected_plugin:
            return []
        return list(map((lambda plugin: plugin.name), selected_plugin))

    def init_plugin_config(self, user_name: str) -> PluginConfig:
        plugin_config = self.config_storage.read_config(user_name)
        plugin_name = plugin_config.selected
        if not plugin_name:
            plugin_name = plugin_config.default
        for plugin_to_select in plugin_name:
            self.select_plugin(plugin_to_select, user_name)
        return plugin_config

    def get_agent_descriptor(self, plugin_to_select) -> Optional[AgentDescriptor]:
        all_plugins = self.all_plugins()

        for plugin in all_plugins:
            if plugin_to_select in (plugin.name, plugin.pkg_name):
                return plugin
        return None

    def select_plugin(self, plugin_to_select: str, user_name: str) -> Optional[pkg.ModuleInfo]:
        agent_descriptor_selected = self.get_agent_descriptor(plugin_to_select)
        if agent_descriptor_selected is None:
            return None

        for module in pkg.iter_modules(self.get_path()):
            if module.name == agent_descriptor_selected.pkg_name:
                self.__select_plugin_for_user(module, user_name)
                if agent_descriptor_selected.pkg_name not in self.__plugins:
                    self.start_agent(agent_descriptor_selected)
                return module

        return None

    def unselect_plugin(self, plugin_to_select: str, user_name: str) -> Optional[pkg.ModuleInfo]:
        agent_descriptor_selected = self.get_agent_descriptor(plugin_to_select)
        if agent_descriptor_selected is None:
            return None

        for module in pkg.iter_modules(self.get_path()):
            if module.name == agent_descriptor_selected.pkg_name:
                self.__unselect_plugin_for_user(module, user_name)
                return module

        return None

    def __select_plugin_for_user(self, plugin_to_select, user_name):
        if user_name in self.__selected_plugin:
            if plugin_to_select not in self.__selected_plugin[user_name]:
                self.__selected_plugin[user_name].append(plugin_to_select)
        else:
            self.__selected_plugin[user_name] = [plugin_to_select]

    def __unselect_plugin_for_user(self, plugin_to_select, user_name):
        if user_name in self.__selected_plugin and plugin_to_select in self.__selected_plugin[user_name]:
            self.__selected_plugin[user_name].remove(plugin_to_select)

    def __get_selected_by_user(self, user_name) -> Optional[List[pkg.ModuleInfo]]:
        if user_name in self.__selected_plugin:
            return self.__selected_plugin[user_name]
        return None

    def reload(self):
        self.__plugins.clear()
        self.preload_plugins()
