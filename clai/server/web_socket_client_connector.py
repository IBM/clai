#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import asyncio
import websockets

from clai.server.client_connector import ClientConnector
from clai.server.command_message import StateDTO, Action
from clai.server.state_mapper import process_message


# pylint: disable=too-few-public-methods
class WebSocketClientConnector(ClientConnector):
    DEFAULT_HOST = "ws://clai-server-test.mybluemix.net"

    def __init__(self, host: str = DEFAULT_HOST):
        self.host = host

    def send(self, message: StateDTO) -> Action:
        response = asyncio.get_event_loop().run_until_complete(
            self.__send_message(message)
        )
        return response

    async def __send_message(self, message: StateDTO):
        async with websockets.connect(self.host) as websocket:
            await websocket.send(str(message.json()))

            received_data = await websocket.recv()
            return process_message(received_data)
