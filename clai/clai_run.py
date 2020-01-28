#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import errno
import socket

from clai.server.clai_server import ClaiServer
from clai.server.web_socket_server_connector import WebSocketServerConnector

START_DIRECTIVE = 'start'
NEW_DIRECTIVE = 'new'


def is_port_busy(host, port, reconnect):
    socket_to_check = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        socket_to_check.bind((host, port))
    except socket.error as exception:
        if exception.errno == errno.EADDRINUSE:
            if not reconnect:
                print("Port is already in use")
            return True

        print(f'something else raised in the socket: {exception}')
    finally:
        socket_to_check.close()

    return False


def create_server_socket(host, port, websocket):
    if websocket:
        server = ClaiServer(connector=WebSocketServerConnector())
    else:
        server = ClaiServer()

    server.init_server()
    server.create_socket(host, port)
    server.listen_client_sockets()
    print(f"server created in host: {host} and port: {port}")


def launcher_server(host, port, directive, websocket):
    if directive == NEW_DIRECTIVE:
        if not is_port_busy(host, port, False):
            create_server_socket(host, port, websocket)
        else:
            print('The server is up yet')
    if directive == START_DIRECTIVE:
        print(f"starting CLAI")
        while is_port_busy(host, port, True):
            print('')
        create_server_socket(host, port, websocket)
