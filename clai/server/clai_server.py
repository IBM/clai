#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

#!/usr/bin/env python3
# pylint: disable=invalid-name,redefined-outer-name
import json

from clai.datasource.action_remote_storage import ActionRemoteStorage
from clai.datasource.server_status_datasource import current_status_datasource, ServerStatusDatasource
from clai.datasource.stats_tracker import StatsTracker
from clai.server.agent_datasource import AgentDatasource
from clai.server.command_message import State, Action, StateDTO
from clai.server.message_handler import MessageHandler
from clai.server.server_connector import ServerConnector
from clai.server.socket_server_connector import SocketServerConnector


# pylint: disable=too-many-arguments
class ClaiServer:

    # pylint: disable=too-many-arguments
    def __init__(self,
                 server_status_datasource: ServerStatusDatasource = current_status_datasource,
                 connector: ServerConnector = SocketServerConnector(current_status_datasource),
                 agent_datasource=AgentDatasource()
                 ):
        self.connector = connector
        self.agent_datasource = agent_datasource
        self.server_status_datasource = server_status_datasource
        self.remote_storage = ActionRemoteStorage()
        self.message_handler = MessageHandler(server_status_datasource, agent_datasource=agent_datasource)
        self.stats_tracker = StatsTracker()

    def init_server(self):
        self.message_handler.init_server()
        self.server_status_datasource.running = True
        self.remote_storage.start(self.agent_datasource)
        self.stats_tracker.start(self.agent_datasource)

    @staticmethod
    def serialize_message(data) -> State:
        StateDTO.update_forward_refs()
        dto = StateDTO(**json.loads(data))
        return State(
            command_id=dto.command_id,
            user_name=dto.user_name,
            command=dto.command,
            root=dto.root,
            processes=dto.processes,
            file_changes=dto.file_changes,
            network=dto.network,
            result_code=dto.result_code,
            stderr=dto.stderr
        )

    def create_socket(self, host, port):
        self.connector.create_socket(host, port)

    def listen_client_sockets(self):
        self.connector.loop(self.process_message)
        self.remote_storage.wait()
        self.stats_tracker.wait()

    def process_message(self, received_data: bytes) -> Action:
        message = self.serialize_message(received_data)
        return self.message_handler.process_message(message)
