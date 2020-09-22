#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#
from clai.server.agent_datasource import AgentDatasource
from clai.server.command_message import State, Action
from clai.server.command_runner.command_runner import CommandRunner

# pylint: disable=too-few-public-methods
from clai.tools.colorize_console import Colorize


class ClaiReloadCommandRunner(CommandRunner):
    def __init__(self, agent_datasource: AgentDatasource):
        self.agent_datasource = agent_datasource

    def execute(self, state: State) -> Action:
        self.agent_datasource.reload()

        text = Colorize().complete().append("Plugins reloaded.\n").to_console()

        return Action(
            suggested_command=":",
            execute=True,
            description=text,
            origin_command=state.command,
        )
