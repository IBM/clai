#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import abc
from typing import Callable


class ServerConnector(abc.ABC):
    @abc.abstractmethod
    def create_socket(self, host: str, port: int):
        '''This method inialize the connection'''

    @abc.abstractmethod
    def loop(self, process_message: Callable[[bytes], str]):
        '''This is the loop method for manage the connection'''
