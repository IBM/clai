#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import abc

from clai.server.command_message import StateDTO, Action


# pylint: disable=too-few-public-methods
class ClientConnector(abc.ABC):
    @abc.abstractmethod
    def send(self, message: StateDTO) -> Action:
        """Send a message to the server using a DTO"""
