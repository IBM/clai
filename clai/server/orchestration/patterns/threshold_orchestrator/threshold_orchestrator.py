#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from typing import Optional, List, Union

from clai.server.orchestration.orchestrator import Orchestrator
from clai.server.command_message import State, Action, TerminalReplayMemoryComplete
from clai.server.command_message import TerminalReplayMemory


# pylint: disable=too-many-arguments,unused-argument
class Thresholder(Orchestrator):

    def __init__(self):
        super(Thresholder, self).__init__()

        self._threshold_pre = {}
        self._threshold_post = {}
        self._default_threshold = 0.2

        self.load_state()

    def get_orchestrator_state(self):
        state = {
            'threshold_pre': self._threshold_pre,
            'threshold_post': self._threshold_post
        }
        return state

    def load_state(self):
        state = self.load()
        self._threshold_pre = state.get('threshold_pre', {})
        self._threshold_post = state.get('threshold_post', {})

    def choose_action(self, command: State, agent_names: List[str],
                      candidate_actions: Optional[List[Union[Action, List[Action]]]],
                      force_response: bool, pre_post_state: str) -> Optional[Action]:
        if not candidate_actions:
            return None

        if isinstance(candidate_actions, Action):
            candidate_actions = [candidate_actions]

        max_confscore = float("-inf")
        best_action = None
        threshold_map = self._threshold_pre if pre_post_state == "pre" else self._threshold_post

        for i, action in enumerate(candidate_actions):
            agent = agent_names[i]

            if agent not in threshold_map:
                threshold_map[agent] = self._default_threshold

            confidence = self.__calculate_confidence__(action)
            if confidence > threshold_map[agent] and confidence > max_confscore:
                max_confscore = confidence
                best_action = action
        return best_action

    def record_transition(self, prev_state: TerminalReplayMemoryComplete,
                          current_state_pre: TerminalReplayMemory):

        prev_state_post = prev_state.post_replay
        if prev_state_post.command.action_suggested is None or \
                prev_state_post.command.action_suggested.suggested_command == self.noop_command:
            return

        agent_executed = prev_state_post.command.action_suggested.agent_owner
        if prev_state_post.command.suggested_executed is True:
            self._threshold_pre[agent_executed] = self._threshold_pre.get(
                agent_executed, self._default_threshold) - 0.02
        else:
            self._threshold_pre[agent_executed] = self._threshold_pre.get(
                agent_executed, self._default_threshold) + 0.05

        self.save()
