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
# tellina_endpoint = 'https://tellina-server.mybluemix.net/message'
# tellina_endpoint = 'http://184.172.250.6:30320/api/translate'
tellina_endpoint = 'http://nlc2cmd.sl.res.ibm.com:8000/api/translate'

# dummy_output = {
# "confidence": "0.0",
# "response": "du -a . | sort -n -r | head"
# }

class TELLINA(Agent):
    def __init__(self):
        super(TELLINA, self).__init__()
        # self.service = Service()

    def get_next_action(self, state: State) -> Action:

        # user typed in, in natural language
        command = state.command

        try:

            # logger.info("#### In Tellina skill, prior to call to endpoint #####")
            # logger.info("Command passed in: " + command)

            # TODO: ADD A TRY HERE BEFORE THE POST TO CATCH BROKENPIPEEXCEPTION

            ## Needs to be a post request since service/endpoint is configured for post
            endpoint_comeback = requests.post(tellina_endpoint, json={'command': command}).json()
            # endpoint_comeback = dummy_output

            ## tellina endpoint must return a json with
            ## keys "response" and "confidence"

            # dummy_high_confidence = 0.9

            # logger.info("##### In Tellina skill, after call, logging contents of callback from kube deployed tellina post #####")
            # logger.info(endpoint_comeback)
            # logger.info("Response: " + endpoint_comeback['response'])
            # logger.info("Confidence: " + endpoint_comeback['confidence'])
            # logger.info("Dummy High Confidence: " + str(dummy_high_confidence))

            response = endpoint_comeback['response']
            confidence = float(endpoint_comeback['confidence'])
            # confidence = dummy_high_confidence  # sending a dummy high confidence for test

            return Action(
                suggested_command=NOOP_COMMAND,
                execute=True,
                description=Colorize().info().append(response).to_console(),
                confidence=confidence)

        except Exception as ex:
            return [ { "text" : "Method failed with status " + str(ex) }, 0.0 ]
