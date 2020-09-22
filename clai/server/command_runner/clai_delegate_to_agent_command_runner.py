#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from typing import List

from clai.server.command_message import State, Action
from clai.server.command_runner.agent_command_runner import AgentCommandRunner
from clai.server.command_runner.clai_help_command_runner import ClaiHelpCommandRunner
from clai.server.command_runner.command_runner import CommandRunner, PostCommandRunner

# pylint: disable=too-few-public-methods
CLAI_COMMAND_NAME = "clai"


class ClaiDelegateToAgentCommandRunner(CommandRunner, PostCommandRunner):
    def __init__(self, agent: AgentCommandRunner):
        self.agent = agent

    def execute(self, state: State) -> Action:
        command_to_check = state.command.replace(CLAI_COMMAND_NAME, "", 1).strip()
        state.command = command_to_check

        if not command_to_check.strip():
            return ClaiHelpCommandRunner().execute(state)

        if command_to_check.startswith('"'):
            possible_agents = command_to_check.split('"')[1::2]
            if possible_agents:
                agent_name = possible_agents[0]
                self.agent.force_agent = agent_name
                state.command = command_to_check.replace(
                    f'"{agent_name}"', "", 1
                ).strip()

        action = self.agent.execute(state)
        if not action:
            return ClaiHelpCommandRunner().execute(state)

        if isinstance(action, Action):
            if action.is_same_command() and not action.description:
                return ClaiHelpCommandRunner().execute(state)

        if isinstance(action, List):
            diffent_actions = list(
                filter(lambda value: not value.is_same_action(), action)
            )
            if not diffent_actions:
                return ClaiHelpCommandRunner().execute(state)

        return action

    def execute_post(self, state: State) -> Action:
        return self.agent.execute_post(state)
