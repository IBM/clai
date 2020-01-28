#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.server.clai_message_builder import create_message_help
from clai.server.command_message import State, Action
from clai.server.command_runner.command_runner import CommandRunner


# pylint: disable=too-few-public-methods
class ClaiHelpCommandRunner(CommandRunner):

    def execute(self, state: State) -> Action:
        return create_message_help()
