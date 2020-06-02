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

from rltk import instantiate_from_file      # pylint: disable=import-error

from clai.server.orchestration.orchestrator import Orchestrator
from clai.server.command_message import State, Action
from clai.server.command_message import TerminalReplayMemory, TerminalReplayMemoryComplete

from . import warm_start_datagen


# pylint: disable=too-many-arguments,unused-argument
class RLTKBandit(Orchestrator):

    def __init__(self):
        super(RLTKBandit, self).__init__()

        self._config_filepath = os.path.join(Path(__file__).parent.absolute(), 'config.yml')
        self._noop_action = 'NOOP'
        self._noop_confidence = 0.25
        self._agent = None
        self._n_actions = None
        self._action_order = None
        self._warm_start = None

        self.load_state()
        self.warm_start_orchestrator()

    def get_orchestrator_state(self):

        state = {
            'agent': self._agent,
            'action_order': self._action_order,
            'warm_start': self._warm_start
        }
        return state

    def load_state(self):

        state = self.load()
        default_action_order = {self._noop_action: 0}

        self._agent = state.get('agent', None)
        if self._agent is None:
            self._agent = instantiate_from_file(self._config_filepath)

        self._action_order = state.get('action_order', None)
        if self._action_order is None:
            self._action_order = default_action_order

        self._n_actions = self._agent.num_actions
        self._warm_start = state.get('warm_start', True)

    def warm_start_orchestrator(self):
        """
        Warm starts the orchestrator (pre-trains the weights) to suit a
        particular profile
        """

        def noop_setup():
            profile = 'noop-always'
            kwargs = {
                'n_points': 1000,
                'context_size': self._n_actions,
                'noop_position': 0
            }
            return profile, kwargs

        def ignore_skill_setup(skill_name):
            self.__add_to_action_order__(skill_name)
            profile = 'ignore-skill'
            kwargs = {
                'n_points': 1000,
                'context_size': self._n_actions,
                'skill_idx': self._action_order[skill_name]
            }
            return profile, kwargs

        def max_orchestrator_setup():
            profile = 'max-orchestrator'
            kwargs = {
                'n_points': 1000,
                'context_size': self._n_actions
            }
            return profile, kwargs

        # profile, kwargs = ignore_skill_setup(skill_name=self._NOOP_ACTION)
        profile, kwargs = max_orchestrator_setup()
        tids, contexts, arm_rewards = warm_start_datagen.get_warmstart_data(
            profile, **kwargs
        )

        self._agent.warm_start(tids, arm_rewards, contexts=contexts)
        self._warm_start = False

        self.save()

    def choose_action(self,
                      command: State, agent_names: List[str],
                      candidate_actions: Optional[List[Union[Action, List[Action]]]],
                      force_response: bool,
                      pre_post_state: str):

        if not candidate_actions:
            return None

        if isinstance(candidate_actions, Action):
            candidate_actions = [candidate_actions]

        context = self.__build_context__(candidate_actions)
        action_idx = self._agent.choose(t_id=command.command_id,
                                        context=context,
                                        num_arms=1)
        suggested_action = self.__choose_action__(action_idx[0], candidate_actions)

        if suggested_action is None:
            suggested_action = Action(suggested_command=command.command)

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

        context = [0.0] * self._n_actions

        noop_pos = self._action_order[self._noop_action]
        context[noop_pos] = self._noop_confidence

        for action in candidate_actions:

            self.__add_to_action_order__(action.agent_owner)

            pos = self._action_order[action.agent_owner]
            conf = self.__calculate_confidence__(action)
            context[pos] = conf

        return np.array(context, dtype=np.float)

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

        if suggested_agent == self._noop_action or suggested_agent is None:
            return None

        for action in candidate_actions:
            if action.agent_owner == suggested_agent:
                return action

    # pylint: disable=no-self-use
    def __compute_pre_transition_reward__(self,
                                          prev_state: TerminalReplayMemory,
                                          post_state: TerminalReplayMemory):
        return 0

    # pylint: disable=no-self-use
    def __compute_post_transition_reward__(self,
                                           prev_state: TerminalReplayMemory,
                                           post_state: TerminalReplayMemory):
        return 0
