#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

''' imports '''
from clai.server.agent import Agent
from clai.server.command_message import State, Action, NOOP_COMMAND

from clai.server.plugins.gitbot.service import Service
from clai.tools.colorize_console import Colorize

import json
import os


''' globals '''
_real_path = '/'.join(os.path.realpath(__file__).split('/')[:-1])
_path_to_config_file = _real_path + '/config.json'

_config = json.loads( open(_path_to_config_file).read() )

_path_to_rasa_model = "{}/rasa/models/{}".format(_real_path, _config["path_to_rasa_saved_model"])
_rasa_port_number = _config["rasa_port_number"]


''' main gitbot class '''
class GITBOT(Agent):
    def __init__(self):
        super(GITBOT, self).__init__()
        self.service = Service()

        # KILL THE RASA SERVER
        # WARNING KILLS OTHERS TOO
        # os.system('lsof -t -i tcp:{} | xargs kill'.format(_rasa_port_number))
        # BRING UP THE RASA SERVER
        # os.system('rasa run --enable-api -m {} -p {}'.format(_path_to_rasa_model, _rasa_port_number))

    ''' pre execution processing '''
    def get_next_action(self, state: State) -> Action:
        command = state.command
        response = self.service(command)

        # action1 = Action(
        #     suggested_command="git branch | tee {}".format("/Users/tathagata/tmp.log"),
        #     execute=True,
        #     description="log: action1",
        #     confidence=1.0)

        # action2 = Action(
        #     suggested_command="cat /Users/tathagata/tmp.log",
        #     execute=True,
        #     description="log: action2",
        #     confidence=1.0)

        response_objects = [] 

        for command in response:
            response_objects.append(Action(
                suggested_command=command,
                execute=False, 
                description=command,
                confidence=1.0)
            )

        return response_objects

    ''' pre execution processing '''
    def post_execute(self, state: State) -> Action:
        # for a more sophisticated state change mechanism, see the ibmcloud skill
        if state.result_code == '0': self.service.parse_command(state.command, stdout = "")
        return Action(suggested_command=NOOP_COMMAND)

    def save_agent(self) -> bool:
        # KILL THE RASA SERVER
        os.system('lsof -t -i tcp:{} | xargs kill'.format(_rasa_port_number))

        # return to original destruction method
        super().save_agent()

