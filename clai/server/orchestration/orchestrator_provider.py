#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#
from abc import ABC
import importlib
import inspect
import pkgutil as pkg

from clai.server.agent_datasource import AgentDatasource
from clai.server.orchestration.orchestrator import Orchestrator

# pylint: disable=too-few-public-methods
import clai.server.orchestration.patterns as pattern


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

    def all_orchestrator(self):
        list_values = list(map(lambda value: value.name, pkg.iter_modules(self.get_path())))
        return list_values

    @staticmethod
    def get_path():
        return pattern.__path__
