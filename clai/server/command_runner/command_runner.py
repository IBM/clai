#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from abc import ABC, abstractmethod
from typing import Union, List

from clai.server.command_message import State, Action


# pylint: disable=too-few-public-methods
class CommandRunner(ABC):
    @abstractmethod
    def execute(self, state: State) -> Union[Action, List[Action]]:
        """Execute the command and return a valid Action"""


class PostCommandRunner(ABC):
    @abstractmethod
    def execute_post(self, state: State) -> Action:
        """post Execute the command and return a valid Action"""
