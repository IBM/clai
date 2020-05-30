#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.server.agent import Agent
from clai.server.command_message import State, Action, NOOP_COMMAND
from clai.tools.colorize_console import Colorize

class GITBOT(Agent):
    def __init__(self):
        super(GITBOT, self).__init__()

    def get_next_action(self, state: State) -> Action:
        command = state.command
        response, confidence = ["ls", 0.0]

        return Action(
            suggested_command=NOOP_COMMAND,
            execute=True,
            description=Colorize().info().append(response).to_console(),
            confidence=confidence)
