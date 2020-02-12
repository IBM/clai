#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import multiprocessing as mp
from typing import Optional, List, Union

import requests

from clai.remote_storage.model_api import TerminalReplayMemoryApi, StateApi, RecordToSendApi
from clai.server.agent_datasource import AgentDatasource
from clai.server.command_message import TerminalReplayMemory, Action, State
from clai.server.logger import current_logger as logger
from clai.tools.anonymizer import Anonymizer

URL_SERVER = "https://us-south.functions.cloud.ibm.com/" \
             "api/v1/web/85360624-31b1-45cd-be6e-562692d2484a/default/" \
             "store_bashbot_command.json"


class ActionRemoteStorage:
    _instance = None

    manager = None
    queue = None
    consumer_task = None
    pool = None
    report_enable = None
    anonymizer = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ActionRemoteStorage, cls).__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self):
        self.manager = mp.Manager()
        self.queue = self.manager.Queue()
        self.consumer_task = None
        self.pool = mp.Pool(1)
        self.report_enable = False
        self.anonymizer = Anonymizer()

    @staticmethod
    def consumer(queue):
        while True:
            data = queue.get()

            if data is None:
                break

            logger.info(f"consume: {data}")
            headers = {'Content-type': 'application/json'}
            response = requests.post(url=URL_SERVER, data=data, headers=headers)
            logger.info(f"[Sent] {response.status_code} message {response.text}")
            queue.task_done()
        logger.info("----STOP CONSUMING-----")

    def start(self, agent_datasource: AgentDatasource):
        logger.info(f"-Start sender-")
        self.report_enable = agent_datasource.get_report_enable()
        if self.report_enable:
            self.consumer_task = self.pool.map_async(self.consumer, (self.queue,))

    def wait(self):
        if self.report_enable:
            self.queue.put(None)
            self.consumer_task.wait(timeout=3)

    def store(self, message: TerminalReplayMemory):
        if not self.report_enable:
            return

        try:
            command = message.command
            message_as_json = TerminalReplayMemoryApi(
                command=self.__parse_state__(command, self.anonymizer),
                agent_names=message.agent_names,
                candidate_actions=self.__parse_actions__(message.candidate_actions),
                force_response=str(message.force_response),
                suggested_command=self.__parse_actions__(message.suggested_command),
            )

            logger.info(f"store -> {message.command.command_id}")

            message_to_send = RecordToSendApi(
                bashbot_info=message_as_json
            )
            self.queue.put(message_to_send.json())
        # pylint: disable=broad-except
        except Exception as err:
            logger.info(f"error sending: {err}")

    @staticmethod
    def __parse_state__(command: State, anonymizer: Anonymizer):
        command_api = StateApi()
        command_api.command_id = command.command_id
        command_api.user_name = anonymizer.anonymize(command.user_name)
        command_api.command = command.command
        command_api.root = command.root
        command_api.processes = command.processes
        command_api.file_changes = command.file_changes
        command_api.network = command.network
        command_api.result_code = command.result_code
        command_api.stderr = command.stderr
        return command_api

    @staticmethod
    def __parse_actions__(candidate_actions: Optional[List[Union[Action, List[Action]]]]):
        if not candidate_actions:
            return []

        if isinstance(candidate_actions, Action):
            return [candidate_actions]

        return candidate_actions
