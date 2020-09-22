#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.server.agent import Agent
from clai.server.command_message import State, Action
from clai.tools.colorize_console import Colorize

from thefuck.types import Command
from thefuck.conf import settings
from thefuck.corrector import get_corrected_commands


class FixBot(Agent):
    """
    Fixes the last executed command by running it through the `thefuck` plugin
    """

    def __init__(self):
        super(FixBot, self).__init__()
        pass

    def get_next_action(self, state: State) -> Action:
        return Action(suggested_command=state.command)

    def post_execute(self, state: State) -> Action:

        if state.result_code == '0':
            return Action(suggested_command=state.command)

        cmd = str(state.command)
        stderr = str(state.stderr)

        try:
            # Get corrected command from `thefuck` bot
            settings.init()
            cmd = Command(cmd, stderr)
            cmd_corrected = get_corrected_commands(cmd)

            cmd_to_run = next(cmd_corrected).script
        except Exception:
            return Action(suggested_command=state.command,
                          confidence=0.1)
        else:
            return Action(
                description=Colorize()
                .info()
                .append("Maybe you want to try: {}".format(cmd_to_run))
                .to_console(),
                confidence=0.8
            )
