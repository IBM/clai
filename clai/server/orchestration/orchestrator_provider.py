#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from abc import ABC
import importlib
import inspect

from clai.server.orchestration.orchestrator import Orchestrator


# pylint: disable=too-few-public-methods
class OrchestratorProvider(ABC):

    @staticmethod
    def get_orchestrator_instance(orchestrator_name: str):
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
                return class_member()

        return None
