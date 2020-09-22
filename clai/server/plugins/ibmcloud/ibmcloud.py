#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.server.agent import Agent
from clai.server.command_message import State, Action, NOOP_COMMAND

from urllib import request, parse
import json, os

# pylint: disable=too-few-public-methods
from clai.tools.colorize_console import Colorize

# import kube services, planner, etc. from ibmcloud.py
from clai.server.plugins.ibmcloud.helper import KubeExe
from clai.server.logger import current_logger as logger


class IBMCloud(Agent):
    def __init__(self):
        super(IBMCloud, self).__init__()

        self.exe = KubeExe()
        self.intents = ["deploy to kube", "build yaml", "run Dockerfile"]

    def get_next_action(self, state: State) -> Action:

        # to be ultimately replaced by a suitable intent recognizer
        # refer to the nlc2cmd skill for an example of a NLC layer
        if state.command in self.intents:

            # deploy to kube deploys local Dockerfile to your ibmcloud
            # run Dockerfile brings up an application locally
            self.exe.set_goal(state.command)

            # this is the sequence of actions that achieves the user's goal
            plan = self.exe.get_plan()

            if plan:

                logger.info("####### log plan inside ibmcloud ########")
                logger.info(plan)

                action_list = []
                for action in plan:
                    # translate from actions in the planner's domain to Action Class
                    action_object = self.exe.execute_action(action)
                    # some actions may have null executions (internal to the reasoning engine)
                    if action_object:
                        action_list.append(action_object)

                return action_list

            else:
                return Action(
                    suggested_command=NOOP_COMMAND,
                    execute=True,
                    description=Colorize()
                    .info()
                    .append("Sorry could not find a plan to help! :-(")
                    .to_console(),
                    confidence=1.0,
                )

        # does not do anything else by default
        else:
            return Action(suggested_command=NOOP_COMMAND)

    def post_execute(self, state: State) -> Action:

        # keep track of state changes
        if state.result_code == "0":
            # need stdout for state monitoring
            self.exe.parse_command(state.command, stdout="")

        return Action(suggested_command=NOOP_COMMAND)
