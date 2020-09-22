#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

""" imports """
from clai.server.agent import Agent
from clai.server.command_message import State, Action, NOOP_COMMAND

from clai.server.plugins.gitbot.service import Service
from clai.tools.colorize_console import Colorize

import os

""" main gitbot class """


class GITBOT(Agent):
    def __init__(self):
        super(GITBOT, self).__init__()
        self.service = Service()

        # KILL THE RASA SERVER
        # WARNING KILLS OTHERS TOO
        # os.system('lsof -t -i tcp:{} | xargs kill'.format(_rasa_port_number))
        # BRING UP THE RASA SERVER
        # os.system('rasa run --enable-api -m {} -p {}'.format(_path_to_rasa_model, _rasa_port_number))

    """ pre execution processing """

    def get_next_action(self, state: State) -> Action:
        command = state.command
        return self.service(command)

    """ pre execution processing """

    def post_execute(self, state: State) -> Action:
        # for a more sophisticated state change mechanism, see the ibmcloud skill
        if state.result_code == "0":
            self.service.parse_command(state.command, stdout="")
        return Action(suggested_command=NOOP_COMMAND)

    def save_agent(self) -> bool:
        # KILL THE RASA SERVER
        os.system("lsof -t -i tcp:{} | xargs kill".format(_rasa_port_number))

        # return to original destruction method
        super().save_agent()
