#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.server.agent import Agent
from clai.server.command_message import State, Action, NOOP_COMMAND
from clai.tools.colorize_console import Colorize

from clai.server.logger import current_logger as logger

import requests

''' globals '''
tellina_endpoint = 'http://nlc2cmd.sl.res.ibm.com:8000/api/translate'


class TELLINA(Agent):
    def __init__(self):
        super(TELLINA, self).__init__()

    def get_next_action(self, state: State) -> Action:

        # user typed in, in natural language
        command = state.command

        try:

            ## Needs to be a post request since service/endpoint is configured for post
            endpoint_comeback = requests.post(tellina_endpoint, json={'command': command}).json()
            ## tellina endpoint must return a json with

            # tellina response, the cmd for the user NL utterance
            response = endpoint_comeback['response']
            # the confidence; the tellina endpoint currently returns 0.0
            confidence = float(endpoint_comeback['confidence'])

            return Action(
                suggested_command=NOOP_COMMAND,
                execute=True,
                description=Colorize().info().append(response).to_console(),
                confidence=confidence)

        except Exception as ex:
            return [ { "text" : "Method failed with status " + str(ex) }, 0.0 ]
