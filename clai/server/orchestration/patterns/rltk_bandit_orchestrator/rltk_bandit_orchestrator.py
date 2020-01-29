#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

"""
This example demonstrates the use of Contextual Thompson Sampling to calibrate the
selector for CLAI skills --> https://pages.github.ibm.com/AI-Engineering/rltk/index.html
"""

from typing import Optional, List, Union
from pathlib import Path

import os
import numpy as np

from rltk import instantiate_from_file

from clai.server.orchestration.orchestrator import Orchestrator
from clai.server.command_message import State, Action
from clai.server.command_message import TerminalReplayMemory, TerminalReplayMemoryComplete


class RLTKBandit(Orchestrator):

    def __init__(self):
        super(RLTKBandit, self).__init__()

        self._config_filepath = os.path.join(Path(__file__).parent.absolute(), 'config.yml')
        self._NOOP_ACTION = 'NOOP'
        self._NOOP_CONFIDENCE = 0.5
        self._agent = None
        self._N_ACTIONS = None
        self._action_order = None

        self.load_state()

    def get_orchestrator_state(self):

        state = {
            'agent': self._agent,
            'action_order': self._action_order
        }
        return state

    def load_state(self):

        state = self.load()
        default_action_order = {self._NOOP_ACTION: 0}

        self._agent = state.get('agent', instantiate_from_file(self._config_filepath))
        self._N_ACTIONS = self._agent.num_actions
        self._action_order = state.get('action_order', default_action_order)

    def choose_action(self, command: State, agent_names: List[str],
                      candidate_actions: Optional[List[Union[Action, List[Action]]]],
                      force_response: bool, pre_post_state: str):

        if not candidate_actions:
            return None

        if isinstance(candidate_actions, Action):
            candidate_actions = [candidate_actions]

        context = self.__build_context__(candidate_actions)
        action_idx = self._agent.choose(t_id=command.command_id,
                                        context=context,
                                        num_arms=1)
        suggested_action = self.__choose_action__(action_idx, candidate_actions)
        return suggested_action

    def record_transition(self,
                          prev_state: TerminalReplayMemoryComplete,
                          current_state_pre: TerminalReplayMemory):

        pre_transition_reward = self.__compute_pre_transition_reward__(
            prev_state.pre_replay, prev_state.post_replay
        )

        post_transition_reward = self.__compute_post_transition_reward__(
            prev_state.post_replay, current_state_pre
        )

        self._agent.observe(prev_state.pre_replay.command.command_id,
                            pre_transition_reward)

        self._agent.observe(prev_state.post_replay.command.command_id,
                            post_transition_reward)

    def __build_context__(self,
                          candidate_actions: Optional[List[Union[Action, List[Action]]]]
                          ) -> np.array:

        context = np.array([0.0] * self._N_ACTIONS)

        noop_pos = self._action_order[self._NOOP_ACTION]
        context[noop_pos] = self._NOOP_CONFIDENCE

        for action in candidate_actions:

            self.__add_to_action_order__(action.agent_owner)

            pos = self._action_order[action.agent_owner]
            context[pos] = self.__calculate_confidence__(action)

        return context

    def __add_to_action_order__(self, agent_name):

        if agent_name in self._action_order:
            return

        max_action_order = max(self._action_order.values())
        self._action_order[agent_name] = max_action_order + 1

    def __choose_action__(self,
                          action_idx: int,
                          candidate_actions: Optional[List[Union[Action, List[Action]]]]):

        suggested_agent = None
        for agent_name, agent_idx in self._action_order.items():
            if agent_idx == action_idx:
                suggested_agent = agent_name
                break

        if suggested_agent == self._NOOP_ACTION or suggested_agent is None:
            return None

        for action in candidate_actions:
            if action.agent_owner == suggested_agent:
                return action

    def __compute_pre_transition_reward__(self,
                                          prev_state: TerminalReplayMemory,
                                          post_state: TerminalReplayMemory):
        return 0

    def __compute_post_transition_reward__(self,
                                           prev_state: TerminalReplayMemory,
                                           post_state: TerminalReplayMemory):
        return 0
