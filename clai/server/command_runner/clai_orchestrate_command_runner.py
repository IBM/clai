#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.server.clai_message_builder import create_orchestrator_list
from clai.server.command_message import State, Action
from clai.server.command_runner.clean_input import extract_quoted_agent_name
from clai.server.command_runner.command_runner import CommandRunner

# pylint: disable=too-few-public-methods
from clai.server.orchestration.orchestrator_provider import OrchestratorProvider


class ClaiOrchestrateCommandRunner(CommandRunner):
    SELECT_DIRECTIVE = "clai orchestrate"
    __VERBOSE_MODE = "-v"

    def __init__(self, orchestrator_provider: OrchestratorProvider):
        self.orchestrator_provider = orchestrator_provider

    def execute(self, state: State) -> Action:
        orchestrator_to_select = state.command.replace(
            f"{self.SELECT_DIRECTIVE}", ""
        ).strip()

        verbose = False
        if self.__VERBOSE_MODE in orchestrator_to_select:
            verbose = True
            orchestrator_to_select = ""
        else:
            orchestrator_to_select = extract_quoted_agent_name(orchestrator_to_select)

        if orchestrator_to_select:
            self.orchestrator_provider.select_orchestrator(orchestrator_to_select)

        return create_orchestrator_list(
            self.orchestrator_provider.get_current_orchestrator_name(),
            self.orchestrator_provider.all_orchestrator(),
            verbose,
        )
