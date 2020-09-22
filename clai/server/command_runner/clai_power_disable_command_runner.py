#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.datasource.server_status_datasource import ServerStatusDatasource
from clai.server.command_message import State, Action, NOOP_COMMAND
from clai.server.command_runner.command_runner import CommandRunner


# pylint: disable=too-few-public-methods
class ClaiPowerDisableCommandRunner(CommandRunner):
    def __init__(self, server_status_datasource: ServerStatusDatasource):
        self.server_status_datasource = server_status_datasource

    def execute(self, state: State) -> Action:
        if not self.server_status_datasource.is_power():
            text = "You have manual mode already enable, use clai auto to activate it"
        else:
            self.server_status_datasource.set_power(False)
            text = "You have enable the manual mode"

        return Action(
            suggested_command=NOOP_COMMAND,
            origin_command=state.command,
            description=text,
            execute=True,
        )
