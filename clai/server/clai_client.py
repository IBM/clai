#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

#!/usr/bin/env python3
import os
import sys

from clai.server.client_connector import ClientConnector
from clai.server.command_message import (
    Action,
    FilesChangesValues,
    ProcessesValues,
    StateDTO,
)
from clai.server.socket_client_connector import SocketClientConnector
from clai.server.web_socket_client_connector import WebSocketClientConnector
from clai.server.logger import current_logger as logger

DEFAULT_PORT = os.getenv("CLAI_PORT", 8010)
LOCALHOST = "localhost"


# pylint: disable=too-few-public-methods
class ClaiClient:
    def __init__(
        self,
        host: str = LOCALHOST,
        port: int = DEFAULT_PORT,
        connector: ClientConnector = None,
    ):
        self.connector = connector

        if not connector:
            self.connector = SocketClientConnector(host=host, port=port)

        self.port = port
        self.host = host

    def send(self, message: StateDTO) -> Action:
        try:
            return self.connector.send(message)
        # pylint: disable=broad-except
        except Exception as exception:
            logger.info(f"error: {exception}")
            return Action(
                origin_command=message.command, suggested_command=message.command
            )


def send_files(command_id: str, user_name: str, files_values: FilesChangesValues):
    file_state = StateDTO(
        command_id=command_id, user_name=user_name, file_changes=files_values
    )
    clai_client = ClaiClient()
    clai_client.send(file_state)


# pylint: disable=too-many-arguments
def send_command_post_execute(
    command_id: str,
    user_name: str,
    result_code: str,
    stderr: str,
    processes: ProcessesValues,
    host: str = LOCALHOST,
    port: int = DEFAULT_PORT,
) -> Action:
    post_execute_state = StateDTO(
        command_id=command_id,
        user_name=user_name,
        result_code=result_code,
        stderr=stderr,
        processes=processes,
    )
    clai_client = ClaiClient(host=host, port=port)
    return clai_client.send(post_execute_state)


def send_command(
    command_id: str,
    user_name: str,
    command_to_check: str,
    host: str = LOCALHOST,
    port: int = DEFAULT_PORT,
) -> Action:
    StateDTO.update_forward_refs()
    command_to_execute = StateDTO(
        command_id=command_id, user_name=user_name, command=command_to_check
    )
    clai_client = ClaiClient(host=host, port=port)
    return clai_client.send(command_to_execute)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage:", sys.argv[0], "<host> <port> <websocket>")
        sys.exit(1)

    # pylint: disable=unbalanced-tuple-unpacking
    HOST, PORT = sys.argv[1:3]
    WEBSOCKET = False
    if sys.argv[3]:
        WEBSOCKET = sys.argv[3] == "websocket"

    INPUT_VALUE = input("$")
    print(HOST, PORT, WEBSOCKET)
    if WEBSOCKET:
        CLAI_CLIENT = ClaiClient(connector=WebSocketClientConnector(host=HOST))
    else:
        CLAI_CLIENT = ClaiClient(connector=SocketClientConnector(host=HOST, port=PORT))

    VALUE = CLAI_CLIENT.send(
        StateDTO(command_id="4", user_name="user", command=INPUT_VALUE)
    )
    print(f"VALUE: {VALUE}")
    print(f"suggested command: {VALUE.suggested_command}")
    print(f"suggested description: {VALUE.description}")
