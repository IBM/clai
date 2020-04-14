#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.server.agent import Agent
from clai.server.command_message import State, Action, NOOP_COMMAND

import json
from pathlib import Path
import os
import re

# pylint: disable=too-few-public-methods
from clai.tools.colorize_console import Colorize

from clai.server.logger import current_logger as logger

class Linuss(Agent):

    def __init__(self):
        super(Linuss, self).__init__()
        self._config_path = os.path.join(
            Path(__file__).parent.absolute(),
            'equivalencies.json'
        )
        self.equivalencies = self.__read_equivalencies()

    def __read_equivalencies(self):
        logger.info('####### read equivalencies inside linuss ########')
        try:
            with open(self._config_path, 'r') as fileobj:
                equivalencies = json.load(fileobj)

        except Exception as e:
            logger.error(f'Linuss Error: {e}')
            equivalencies = json.load({})

        return equivalencies

    def __build_suggestion(self, command, options, cmd_key) -> any:
        suggestion = NOOP_COMMAND
        description = None
        for option in options:
            if re.search(r'{}'.format(option), command):
                suggestion = re.sub(
                    r'{}'.format(option),
                    self.equivalencies[cmd_key][option]["equivalent"], 
                    command
                )
                description = self.equivalencies[cmd_key][option]["explanation"]

        return suggestion, description

    def get_next_action(self, state: State) -> Action:
        command = state.command

        for cmd in self.equivalencies:            
            if command.startswith(cmd):
                s, d = self.__build_suggestion(command, self.equivalencies[cmd], cmd)
                if s is not None:
                    return Action(
                        suggested_command=s,
                        confidence=0.9, 
                        description=d
                    )
            

        return Action(suggested_command=NOOP_COMMAND)
