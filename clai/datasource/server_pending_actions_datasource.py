#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from typing import Dict, List

from clai.datasource.model.pending_actions import PendingActions
from clai.server.command_message import Action


class ServerPendingActionsDatasource:
    def __init__(self):
        self.__pending_actions: Dict[str, List[PendingActions]] = {}

    def store_pending_actions(
        self, command_id: str, actions: List[Action], user_name: str
    ) -> Action:
        actions_by_user = self.__find_pending_actions_by_user(user_name)
        actions_by_user.append(PendingActions(command_id, actions))
        return self.get_next_action(command_id, user_name)

    def get_next_action(self, command_id: str, user_name: str) -> Action:
        actions_by_user = self.__find_pending_actions_by_user(user_name)
        pending_actions = next(
            filter(lambda x: x.command_id == command_id, actions_by_user), None
        )
        return pending_actions.next()

    def __find_pending_actions_by_user(self, user_name: str) -> List[PendingActions]:
        if user_name not in self.__pending_actions:
            self.__pending_actions[user_name] = []
        return self.__pending_actions[user_name]
