#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import requests
import os
import json
from pathlib import Path

from clai.server.agent import Agent
from clai.server.command_message import Action, State

from clai.server.plugins.manpage_agent.question_detection import QuestionDetection
from clai.server.plugins.manpage_agent import tldr_wrapper


class ManPageAgent(Agent):

    def __init__(self):
        super(ManPageAgent, self).__init__()

        self.question_detection_mod = QuestionDetection()
        self._config = None
        self._API_URL = None

        self.read_config()

    def read_config(self):
        curdir = str(Path(__file__).parent.absolute())
        config_path = os.path.join(curdir, 'config.json')

        with open(config_path, 'r') as f:
            self._config = json.load(f)

        self._API_URL = self._config['API_URL']

    def __call_api__(self, search_text):

        payload = {
            'text': search_text,
            'result_count': 1
        }

        headers = {'Content-Type': "application/json"}

        r = requests.post(self._API_URL, params=payload, headers=headers)

        if r.status_code == 200:
            return r.json()

        return None

    def get_next_action(self, state: State) -> Action:

        cmd = state.command
        is_question = self.question_detection_mod.is_question(cmd)

        if not is_question:
            return Action(
                suggested_command=state.command,
                confidence=0.0
            )

        response = None

        try:
            response = self.__call_api__(cmd)
        except Exception:
            pass

        if response is None or response['status'] != 'success':
            return Action(
                suggested_command=state.command,
                confidence=0.0
            )

        command = response['commands'][-1]
        confidence = response['dists'][-1]

        try:
            cmd_tldr = tldr_wrapper.get_command_tldr(command)
        except Exception as err:
            print('Exception: ' + str(err))
            cmd_tldr = ''

        return Action(
            suggested_command="man {}".format(command),
            confidence=confidence,
            description=cmd_tldr
        )

