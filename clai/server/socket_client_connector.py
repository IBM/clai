#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import selectors
import socket
import traceback
import types
import uuid
from typing import Optional

from clai.server.logger import current_logger as logger
from clai.server.client_connector import ClientConnector
from clai.server.command_message import StateDTO, Action
from clai.server.state_mapper import process_message


# pylint: disable=too-few-public-methods
class SocketClientConnector(ClientConnector):
    def __init__(self, host: str, port: int):
        self.sel = selectors.DefaultSelector()
        self.host = host
        self.port = port
        self.uuid = uuid.uuid4()

    def send(self, message: StateDTO) -> Action:
        try:
            return self._internal_send(message)

        # pylint: disable=broad-except
        except Exception as error:
            logger.info(f"error {error}")
            logger.info(traceback.format_exc())

            return Action(
                origin_command=message.command,
                suggested_command=message.command)
        finally:
            self.close()

    def _internal_send(self, command_to_send):
        self.start_connections(self.host, int(self.port))
        self.write(command_to_send)
        action = self.read()
        if action:
            return action

        return Action(
            origin_command=command_to_send.command,
            suggested_command=command_to_send.command)

    def start_connections(self, host, port):

        server_address = (host, port)

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.setblocking(False)
        client_socket.connect_ex(server_address)
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        data = types.SimpleNamespace(
            connid=self.uuid,
            outb=b'',
        )
        self.sel.register(client_socket, events, data=data)

    def write(self, message: StateDTO):
        events = self.sel.select(timeout=5)
        key = events[0][0]
        client_socket = key.fileobj
        data = key.data
        self.sel.modify(client_socket, selectors.EVENT_WRITE, data)
        logger.info(f'echoing ${data}')
        data.outb = str(message.json())
        sent = client_socket.send(data.outb.encode('utf-8'))
        data.outb = data.outb[sent:]
        self.sel.modify(client_socket, selectors.EVENT_READ, data)

    def read(self) -> Optional[Action]:
        events = self.sel.select(timeout=6)
        if events and events[0]:
            key = events[0][0]
            client_socket = key.fileobj
            received_data = client_socket.recv(4024)
            if received_data:
                message = process_message(received_data)
                return message

        return None

    def close(self):
        self.sel.close()
