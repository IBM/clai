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
from typing import Tuple

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
        params:list[Tuple(str)] = []
        suggestion:str = None
        explanations:list[str] = []
        
        # Tokenize the command string
        tokens:list[str] = command.split()
        idx = 0
        max_idx = len(tokens)-1
        while (idx <= max_idx):
            token:str = tokens[idx]
            
            # Case 1: Token is an option flag
            if re.match(r'-([\w_-]+)', token):
                
                # Case 1a: Token is followed by a non-option parameter
                if idx < max_idx and not re.match(r'-([\w_-]+)', tokens[idx+1]):
                    next_token = tokens[idx+1]
                    params.append((token[1:],next_token))
                    idx = idx + 1   # Don't double-process next token
                
                # Case 1b: Token is not followed by a non-option parameter
                else:
                    params.append((token[1:],None))
            
            # Case 2: Token is a non-option parameter
            elif token != cmd_key:
                params.append((None,token))
            
            idx = idx + 1 # Move on to the next token
            
        # If this command requires full command replacement, start the new
        # command string off with that
        if "" in options:
            suggestion = self.equivalencies[cmd_key][""]["equivalent"]
        else:
            suggestion = cmd_key
        
        # Traverse the command from start to end
        for opt, arg in params:
            if opt is not None:
                # Case 1: We're processing a long option or a single short option
                if opt[0] == '-' or len(opt) == 1:
                    equivalency = self.__get_equavalency(opt, options, cmd_key)
                    if equivalency['equivalent']:
                        suggestion = f"{suggestion} {equivalency['equivalent']}"
                        if 'explanation' in equivalency:
                            explanations.append(equivalency['explanation'])
                    else:
                        explanations.append(f"The -{opt} flag is not available on USS")
                
                # Case 2: We're processing multiple short options strung together
                else:
                    for char in opt:
                        equivalency = self.__get_equavalency(char, options, cmd_key)
                        if equivalency['equivalent']:
                            suggestion = f"{suggestion} {equivalency['equivalent']}"
                            if 'explanation' in equivalency:
                                explanations.append(equivalency['explanation'])
                        else:
                            explanations.append(f"The -{char} flag is not available on USS")
            
            # If we have another non-option parameter to add to the suggested
            # command, do so now
            if arg is not None:
                suggestion = f"{suggestion} {arg}"
        
        if suggestion is not None:
            return Action(
                suggested_command=suggestion,
                confidence=1,
                description='\n'.join(explanations)
            )
        else:
            return Action(suggested_command=NOOP_COMMAND, description=None)
    
    def __get_equavalency(self, target, options, cmd_key) -> dict:
        target = f"-{target}"
        for option in options:
            if option == "":
                pass    # Ignore full-command replacement options
            elif re.search(r'{}'.format(option), target):
                return self.equivalencies[cmd_key][option]
        
        return {"equivalent": target}
        
    def get_next_action(self, state: State) -> Action:
        command = state.command

        for cmd in self.equivalencies:            
            if command.startswith(cmd):
                return self.__build_suggestion(command, self.equivalencies[cmd], cmd)

        return Action(suggested_command=NOOP_COMMAND)