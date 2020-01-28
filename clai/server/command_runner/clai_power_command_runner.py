#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.datasource.server_status_datasource import ServerStatusDatasource
from clai.server.command_message import Action, State, NOOP_COMMAND
from clai.server.command_runner.command_runner import CommandRunner


# pylint: disable=too-few-public-methods
class ClaiPowerCommandRunner(CommandRunner):
    def __init__(self, server_status_datasource: ServerStatusDatasource):
        self.server_status_datasource = server_status_datasource

    def execute(self, state: State) -> Action:
        if self.server_status_datasource.is_power():
            text = 'You have the auto mode already enable, use clai manual to deactivate it'
        else:
            self.server_status_datasource.set_power(True)
            text = 'You have enabled the auto mode'

        return Action(
            origin_command=state.command,
            suggested_command=NOOP_COMMAND,
            description=text,
            execute=True
        )
