#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.server.agent_datasource import AgentDatasource
from clai.server.clai_message_builder import create_message_list
from clai.server.command_message import Action, State
from clai.server.command_runner.command_runner import CommandRunner


# pylint: disable=too-few-public-methods
class ClaiPluginsCommandRunner(CommandRunner):
    __VERBOSE_MODE = "-v"

    def __init__(self, agent_datasource: AgentDatasource):
        self.agent_datasource = agent_datasource

    def execute(self, state: State) -> Action:
        action_to_return = create_message_list(
            self.agent_datasource.get_current_plugin_name(state.user_name),
            self.agent_datasource.all_plugins(),
            self.__VERBOSE_MODE in state.command,
        )
        action_to_return.origin_command = state.command
        return action_to_return
