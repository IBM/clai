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


class GITBOT(Agent):
    def __init__(self):
        super(GITBOT, self).__init__()
        self.service = Service()

    def get_next_action(self, state: State) -> Action:
        command = state.command
        response, confidence = self.service(command)

        action1 = Action(
            suggested_command="git branch | tee {}".format("/Users/tathagata/tmp.log"),
            execute=True,
            description="log: action1",
            confidence=1.0)

        action2 = Action(
            suggested_command="cat /Users/tathagata/tmp.log",
            execute=True,
            description="log: action2",
            confidence=1.0)

        return [action1, action2]

        # return Action(
        #     suggested_command=NOOP_COMMAND,
        #     execute=True,
        #     description=Colorize().info().append(response).to_console(),
        #     confidence=confidence)
