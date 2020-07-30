#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.server.agent import Agent
from clai.server.command_message import State, Action, NOOP_COMMAND
from clai.tools.colorize_console import Colorize

import requests

''' globals '''
gpt3_endpoint = 'http://gpt3server.mybluemix.net/gpt3'


class GPT3(Agent):
    def __init__(self):
        super(GPT3, self).__init__()

    def get_next_action(self, state: State) -> Action:

        # user typed in, in natural language
        command = state.command

        try:

            response = requests.post(gpt3_endpoint, json={'text': command, 'use_cached_prompt' : True}).json()
            response = response['response']

            return Action(
                suggested_command=response,
                execute=False,
                description="Currently GPT-3 does not provide an explanation. Got an idea? Contribute to CLAI!",
                confidence=0.0)

        except Exception as ex:
            return [ { "text" : "Method failed with status " + str(ex) }, 0.0 ]

