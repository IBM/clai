#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from typing import List, Optional

from clai.server.command_message import Action

# pylint: disable=too-few-public-methods
class PendingActions:
    def __init__(self, command_id: str, pending_actions: List[Action]):
        self.command_id = command_id
        self.current_action = 0
        self.pending_actions = pending_actions

    def next(self) -> Optional[Action]:
        if self.current_action >= len(self.pending_actions):
            return None

        action_to_return = self.pending_actions[self.current_action]
        self.current_action += 1

        action_to_return.pending_actions = self.current_action < len(self.pending_actions)

        return action_to_return
