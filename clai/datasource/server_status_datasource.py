#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from collections import deque
from typing import Optional, Dict

from clai.server.command_message import State


class ServerStatusDatasource:
    def __init__(self):
        self.__power = False
        self.__messages_store: Dict[str, deque] = {}
        self.running = False

    def __store_info_by_user(self, message: State, user_name: str):
        messages_by_user = self.__find_messages_by_user(user_name)
        messages_by_user.append(message)

    def __find_messages_by_user(self, user_name: str):
        if user_name not in self.__messages_store:
            self.__messages_store[user_name] = deque(maxlen=50)
        return self.__messages_store[user_name]

    def set_power(self, power: bool):
        self.__power = power

    def is_power(self):
        return self.__power

    def get_last_messages(self, user_name: str):
        return self.__find_messages_by_user(user_name)

    def get_last_message(self, user_name: str) -> State:
        last_message = None
        messages_by_user = self.__find_messages_by_user(user_name)
        if messages_by_user and len(messages_by_user) > 1:
            last_message = messages_by_user[-2]
        return last_message

    def store_info(self, message: State) -> State:
        stored_message = self.find_message_stored(message.command_id, message.user_name)
        if stored_message is not None:
            stored_message.merge(message)
            return stored_message

        self.__store_info_by_user(message, message.user_name)
        return message

    def find_message_stored(self, id_to_find: str, user_mame: str) -> Optional[State]:
        messages_by_user = self.__find_messages_by_user(user_mame)
        return next(filter(lambda x: x.command_id == id_to_find, messages_by_user), None)


# pylint: disable= invalid-name
current_status_datasource = ServerStatusDatasource()
