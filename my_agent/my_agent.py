#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from typing import Union, List

from clai.server.agent import Agent
from clai.server.command_message import State, Action

# pylint: disable=too-few-public-methods
from clai.tools.colorize_console import Colorize
from clai.server.logger import current_logger as logger


class DemoAgent(Agent):

    def get_next_action(self, state: State) -> Union[Action, List[Action]]:
        logger.info("This is my agent")
        if state.command == 'ls':
            return Action(suggested_command="ls -la",
                          description="This is a demo sample that helps to execute the command in better way.",
                          confidence=1
                          )

        if state.command == 'pwd':
            return [Action(suggested_command="ls -la",
                           description="This is a demo sample that helps to execute the command in better way.",
                           confidence=1
                           ),
                    Action(suggested_command="pwd -P",
                           description="This is a demo sample that helps to execute the command in better way.",
                           confidence=1
                           )
                    ]
        if state.previous_execution and state.previous_execution.command == 'ls -4':
            return Action(suggested_command="ls -a",
                          execute=True,
                          confidence=1)

        return Action(suggested_command=state.command)

    def post_execute(self, state: State) -> Action:
        if state.command.startswith('ls') and state.result_code != '0':
            return Action(description=Colorize()
                          .append(f"Are you sure that this command is correct?({state.result_code})\n")
                          .warning()
                          .append(f"Try man ls for more info ")
                          .to_console(),
                          confidence=1
                          )

        return Action(suggested_command=state.command)
