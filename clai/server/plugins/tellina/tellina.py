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


# from clai.server.plugins.tellina.service import Service

import requests

''' globals '''
#tellina_endpoint = 'https://tellina-server.mybluemix.net/message'
tellina_endpoint = 'http://184.172.250.6:30320/api/translate'

class TELLINA(Agent):
    def __init__(self):
        super(TELLINA, self).__init__()
        # self.service = Service()

    def get_next_action(self, state: State) -> Action:

        # user typed in, in natural language
        command = state.command

        try:

            logger.info("#### In Tellina skill, prior to call to endpoint #####")
            logger.info("Command passed in: " + command)

            ## Needs to be a post request since service/endpoint is configured for post
            endpoint_comeback = requests.post(tellina_endpoint, json={'command': command}).json()

            ## tellina endpoint must return a json with
            ## keys "response" and "confidence"

            logger.info("##### In Tellina skill, after call, ogging contents of callback from kube deployed tellina post #####")
            logger.info(endpoint_comeback)
            logger.info("Response: " + endpoint_comeback['response'])
            logger.info("Confidence: " + endpoint_comeback['confidence'])

            response = endpoint_comeback['response']
            confidence = endpoint_comeback['confidence']

            return Action(
                suggested_command=NOOP_COMMAND,
                execute=True,
                description=Colorize().info().append(response).to_console(),
                confidence=confidence)

        except Exception as ex:
            return [ { "text" : "Method failed with status " + str(ex) }, 0.0 ]
