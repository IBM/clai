#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.server.agent import Agent
from clai.server.command_message import State, Action, NOOP_COMMAND

from clai.server.plugins.nlc2cmd.service import Service
from clai.tools.colorize_console import Colorize


class NLC2CMD(Agent):
    def __init__(self):
        super(NLC2CMD, self).__init__()
        self.service = Service()

    def get_next_action(self, state: State) -> Action:

        command = state.command
        data, confidence = self.service(command)
        response = data["text"]

        return Action(
            suggested_command=NOOP_COMMAND,
            execute=True,
            description=Colorize().info().append(response).to_console(),
            confidence=confidence)
