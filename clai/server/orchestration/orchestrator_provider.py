#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#
import configparser
import os
from abc import ABC
import importlib
import inspect
import pkgutil as pkg
from typing import List

from clai.server.agent_datasource import AgentDatasource
from clai.server.orchestration.orchestrator import Orchestrator

# pylint: disable=too-few-public-methods
import clai.server.orchestration.patterns as pattern
from clai.server.orchestration.orchestrator_descriptor import OrchestratorDescriptor


class OrchestratorProvider(ABC):
    def __init__(self, agent_datasource: AgentDatasource):
        self.agent_datasource = agent_datasource
        self.__current_orchestrator_name = None
        self.orchestrator_instances = {}

    def select_orchestrator(self, name: str):
        if name == self.__current_orchestrator_name:
            return

        if name in self.orchestrator_instances:
            self.__current_orchestrator_name = name
        else:
            if self.get_orchestrator_instance(name):
                self.__current_orchestrator_name = name

    def get_current_orchestrator_name(self):
        if not self.__current_orchestrator_name:
            self.get_current_orchestrator()

        return self.__current_orchestrator_name

    def get_current_orchestrator(self):
        if not self.__current_orchestrator_name:
            self.__current_orchestrator_name = self.agent_datasource.get_current_orchestrator()

        if self.__current_orchestrator_name in self.orchestrator_instances:
            return self.orchestrator_instances[self.__current_orchestrator_name]

        return self.get_orchestrator_instance(self.__current_orchestrator_name)

    def get_orchestrator_instance(self, orchestrator_name: str):
        """
        Returns an instance of the requested orchestration pattern
        :param orchestrator_name: Orchestrator pattern package name
        :return: instantiated object of the orchestrator
        """

        orchestrator_mods = importlib.import_module(
            f'clai.server.orchestration.patterns.{orchestrator_name}.{orchestrator_name}',
            package=orchestrator_name
        )

        for _, class_member in inspect.getmembers(orchestrator_mods, inspect.isclass):
            if issubclass(class_member, Orchestrator) and (class_member is not Orchestrator):
                class_member = class_member()
                self.orchestrator_instances[orchestrator_name] = class_member
                return class_member

        return None

    def all_orchestrator(self) -> List[OrchestratorDescriptor]:
        orchestrator_names = list(map(lambda value: value.name, pkg.iter_modules(self.get_path())))

        orchestrators = []
        for orchestrator in orchestrator_names:
            orchestrator_plugin = os.path.join(self.get_path()[0], orchestrator)
            orchestrator_descriptor = self.load_descriptors(orchestrator_plugin, orchestrator)
            if not orchestrator_descriptor.exclude:
                orchestrators.append(orchestrator_descriptor)

        return orchestrators

    @staticmethod
    def load_descriptors(path, name) -> OrchestratorDescriptor:
        file_path = os.path.join(path, "manifest.properties")
        if os.path.exists(file_path):
            config_parser = configparser.ConfigParser()
            config_parser.read(file_path)

            exclude = False
            if config_parser.has_option('DEFAULT', 'exclude'):
                exclude = config_parser.getboolean('DEFAULT', 'exclude')

            description = ""
            if config_parser.has_option('DEFAULT', 'description'):
                description = config_parser.get('DEFAULT', 'description')

            return OrchestratorDescriptor(
                name=name,
                exclude=exclude,
                description=description
            )

        return OrchestratorDescriptor(
            name=name,
            exclude=False,
            description=""
        )

    @staticmethod
    def get_path():
        return pattern.__path__
