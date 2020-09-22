#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import selectors
import socket
import types
from typing import Callable

from clai.datasource.server_status_datasource import ServerStatusDatasource
from clai.server.command_message import Action
from clai.server.server_connector import ServerConnector
from clai.server.logger import current_logger as logger


class SocketServerConnector(ServerConnector):
    BUFFER_SIZE = 4024

    def __init__(self, server_status_datasource: ServerStatusDatasource):
        self.server_status_datasource = server_status_datasource
        self.sel = selectors.DefaultSelector()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def create_socket(self, host: str, port: int):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((host, port))
        self.server_socket.listen()
        logger.info(f"Listening {host} {port}")
        self.server_socket.setblocking(False)

    def loop(self, process_message: Callable[[bytes], Action]):
        self.sel.register(self.server_socket, selectors.EVENT_READ, data=None)
        try:
            while self.server_status_datasource.running:
                events = self.sel.select(timeout=None)
                for key, mask in events:
                    if key.data is None:
                        self.__accept_wrapper(key.fileobj)
                    else:
                        self.__service_connection(key, mask, process_message)
            self.sel.unregister(self.server_socket)
            self.server_socket.close()
        except KeyboardInterrupt:
            logger.info("caught keyboard interrupt, exiting")
        finally:
            logger.info("server closed")
            self.sel.close()

    def __accept_wrapper(self, server_socket):
        connection, address = server_socket.accept()
        connection.setblocking(False)
        data = types.SimpleNamespace(addr=address, inb=b"", outb=b"")
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        self.sel.register(connection, events, data=data)

    def __service_connection(self, key, mask, process_message):
        fileobj = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            data = self.__read(data, fileobj, process_message)
        if mask & selectors.EVENT_WRITE:
            self.__write(data, fileobj)

    @staticmethod
    def __write(data, server_socket):
        if data.outb:
            logger.info(f"sending from client ${data.outb}")
            server_socket.send(data.outb)
            data.outb = b""

    def __read(self, data, server_socket, process_message):
        recv_data = b""
        chewing = True
        logger.info(f"receiving from client")
        while chewing:
            part = server_socket.recv(self.BUFFER_SIZE)
            recv_data += part
            if len(part) < self.BUFFER_SIZE:
                chewing = False

        if recv_data:
            logger.info(f"receiving from client ${recv_data}")
            action = process_message(recv_data)
            data.outb = str(action.json()).encode("utf8")
        else:
            self.sel.unregister(server_socket)
            server_socket.close()
        return data
