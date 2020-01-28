#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

"""
This example demonstrates the use of Contextual Thomspon Sampling to calibrate the
selector for CLAI skills --> https://pages.github.ibm.com/AI-Engineering/bandit-core/
"""

from typing import Optional, List, Union
from pathlib import Path

import os
import numpy
# pylint: disable=import-error
import bandits

from clai.server.orchestration.orchestrator import Orchestrator
from clai.server.command_message import State, Action, TerminalReplayMemoryComplete
from clai.server.command_message import TerminalReplayMemory


# pylint: disable=too-many-arguments,unused-argument
class Bandit(Orchestrator):

    def __init__(self):
        super(Bandit, self).__init__()

        self._path_to_config_file = os.path.join(Path(__file__).parent.absolute(), 'config.yml')
        self._agent = bandits.instantiate_from_file(self._path_to_config_file)
        self._event_number = 0

        self._selected_arm = None
        self._match_threshold = 0.7

        self.load_state()

    def get_orchestrator_state(self):
        state = {
            'self': self._agent,
            'event': self._event_number
        }
        return state

    def load_state(self):
        state = self.load()
        self._agent = state.get('self', bandits.instantiate_from_file(self._path_to_config_file))
        self._event_number = state.get('event', 0)

    def choose_action(self, command: State, agent_names: List[str],
                      candidate_actions: Optional[List[Union[Action, List[Action]]]],
                      force_response: bool, pre_post_state: str) -> Optional[Action]:

        if not candidate_actions:
            return None

        if isinstance(candidate_actions, Action):
            candidate_actions = [candidate_actions]

        self._event_number += 1

        # current context is a vector of confidences
        # in future, extend this with more State and Agent info
        context_dimension = self._agent.serialize()['policy'].dim
        context_data = context_dimension * [0.0]

        for i, candidate_action in candidate_actions:
            context_data[i] = self.__calculate_confidence__(candidate_action)

        context_data = numpy.asarray(context_data)

        self._selected_arm = self._agent.choose(self._event_number, context_data)[0]

        # map arm to action and agent name
        try:
            # index may be out of range
            return candidate_actions[self._selected_arm]
        # pylint: disable=bare-except
        except:
            return None

    def record_transition(self, prev_state: TerminalReplayMemoryComplete,
                          current_state_pre: TerminalReplayMemory):

        prev_state_pre = prev_state.pre_replay
        prev_state_post = prev_state.post_replay

        if prev_state_pre.command.action_suggested is None or \
                prev_state_post.command.action_suggested is None or \
                prev_state_post.command.action_suggested.suggested_command == self.noop_command:
            return

        reward = float(prev_state_post.command.suggested_executed)

        currently_executed_command = current_state_pre.command.command
        all_the_stuff_from_last_execution = prev_state_pre.command.action_suggested.suggested_command \
                                            + prev_state_pre.command.action_suggested.description \
                                            + prev_state_post.command.action_suggested.description

        base = set(currently_executed_command.split())
        reference = set(all_the_stuff_from_last_execution.split())

        # check how much of the current commands is contained in the stuff from last time
        match_score = len(base & reference) / len(base)
        reward += float(match_score > self._match_threshold)

        self._agent.observe(self._event_number, reward)
        self.save()
