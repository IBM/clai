#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.server.agent import Agent
from clai.server.command_message import State, Action, NOOP_COMMAND

import json, os

### globals ###
_real_path = '/'.join(os.path.realpath(__file__).split('/')[:-1])
_data_path = _real_path + '/data/config.json'

class Onboarding(Agent):
    def __init__(self):
        super(Onboarding, self).__init__()

        # load translator
        self.transformer = json.loads(open(_data_path).read())

    def get_next_action(self, state: State) -> Action:

        # user typed in command
        command = state.command

        # use case 1: direct transform
        for item in self.transformer:
            if command.startswith(item):
                command = ' '.join([self.transformer[item]] + command.split()[1:])
                return Action(suggested_command=command, execute=True, confidence=1.0)

        # use case 2: natural language transform
        # call to service that can turn natural language descriptors into commands
        # command, confidence = self.service(state)
        # return Action(suggested_command=command, execute=True, confidence=confidence)
        # refer to nlc2cmd skill

        # use case 3: retrieval transform
        # call to service that can retrieve useful forum post or documentation
        # info, confidence = self.service(state)
        # return Action(suggested_command=NOOP_COMMAND, execute=True, description=info, confidence=confidence)
        # refer to howdoi / helpme skills

        # use case 4: sequence transform
        # call to service that has learned these macros
        # command_list, confidence = self.service(state)
        # refer to ibmcloud skill
        if command.startswith('cd'):
            return [ Action(suggested_command=command, execute=True, confidence=1.0),
                     Action(suggested_command='ls', execute=True, confidence=1.0)
                     ]

        # default execution
        return Action(
            suggested_command=NOOP_COMMAND,
            execute=False,
            description="Onboarding example.",
            confidence=0.0)



