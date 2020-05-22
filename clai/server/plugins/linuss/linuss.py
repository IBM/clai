#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.server.agent import Agent
from clai.server.command_message import State, Action, NOOP_COMMAND

import os
import re
import json
from pathlib import Path

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
            with open(self._config_path, 'r') as json_file:
                equivalencies = json.load(json_file)

        except Exception as e:
            logger.debug(f'Linuss Error: {e}')
            equivalencies = json.load({})

        return equivalencies

    def __build_suggestion(self, command, options, cmd_key) -> any:
        actions = []
        for option in options:
            if re.search(r'{}'.format(option), command):
                replacement_value = None
                if not option:
                    # Case 1: Full command replacement
                    replacement_value = cmd_key
                else:
                    # Case 2: We're replacing an option flag
                    replacement_value = option
                    
                suggestion = re.sub(
                    r'{}'.format(replacement_value),
                    self.equivalencies[cmd_key][option]["equivalent"], 
                    command
                )

                # The confidence is high because these 
                # are pre-determined and we know these are correct
                actions.append(
                    Action(
                        suggested_command=suggestion,
                        confidence=1, 
                        description=self.equivalencies[cmd_key][option]["explanation"]
                    )
                )

        if not actions:
            actions.append(Action(suggested_command=NOOP_COMMAND, description=None))

        return actions

    def get_next_action(self, state: State) -> Action:
        command = state.command

        for cmd in self.equivalencies:            
            if command.startswith(cmd):
                return self.__build_suggestion(command, self.equivalencies[cmd], cmd)

        return Action(suggested_command=NOOP_COMMAND)