#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from typing import Union, List

from clai.datasource.server_status_datasource import ServerStatusDatasource
from clai.server.agent_runner import AgentRunner
from clai.server.command_message import State, Action
from clai.server.command_runner.command_runner import CommandRunner, PostCommandRunner


# pylint: disable=too-few-public-methods
class AgentCommandRunner(CommandRunner, PostCommandRunner):

    def __init__(self, agent_runner: AgentRunner, server_status_datasource: ServerStatusDatasource,
                 ignore_threshold: bool = False):
        self.agent_runner = agent_runner
        self.server_status_datasource = server_status_datasource
        self.ignore_threshold = ignore_threshold
        self.force_agent = None

    def execute(self, state: State) -> Union[Action, List[Action]]:
        action = self.agent_runner.process(state, self.ignore_threshold, self.force_agent)
        if not action:
            action = Action()
        return action

    def execute_post(self, state: State) -> Action:
        action = self.agent_runner.process_post(state, self.ignore_threshold)
        if not action:
            action = Action()
        action.origin_command = state.command
        return action
