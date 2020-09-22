#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

"""
This example demonstrates the use of Contextual Thompson Sampling
to calibrate the selector for CLAI skills
"""

from typing import Optional, List, Union
from pathlib import Path

import os
import json
import numpy as np

from rltk import instantiate_from_file      # pylint: disable=import-error

from clai.server.orchestration.orchestrator import Orchestrator
from clai.server.command_message import State, Action
from clai.server.command_message import TerminalReplayMemory, TerminalReplayMemoryComplete
from clai.server.logger import current_logger as logger

from . import warm_start_datagen


# pylint: disable=too-many-arguments,unused-argument,too-many-instance-attributes
class RLTKBandit(Orchestrator):

    def __init__(self):
        super(RLTKBandit, self).__init__()

        self._config_filepath = os.path.join(Path(__file__).parent.absolute(), 'config.yml')
        self._bandit_config_filepath = os.path.join(Path(__file__).parent.absolute(), 'bandit_config.json')

        self._noop_confidence = None
        self._agent = None
        self._n_actions = None
        self._action_order = None
        self._warm_start = None
        self._warm_start_type = None
        self._warm_start_kwargs = None
        self._reward_match_threshold = None

        self.load_bandit_state()
        self.load_state()
        self.warm_start_orchestrator()

    def load_bandit_state(self):

        with open(self._bandit_config_filepath, 'r') as conf_file:
            bandit_config = json.load(conf_file)

        self._noop_confidence = bandit_config['noop_confidence']
        self._warm_start = bandit_config['warm_start']
        self._warm_start_type = bandit_config['warm_start_config']['type']
        self._warm_start_kwargs = bandit_config['warm_start_config']['kwargs']
        self._reward_match_threshold = bandit_config.get('reward_match_threshold', 0.7)

    def get_orchestrator_state(self):

        state = {
            'agent': self._agent,
            'action_order': self._action_order,
            'warm_start': self._warm_start
        }
        return state

    def load_state(self):

        state = self.load()
        default_action_order = {self.noop_command: 0}

        self._agent = state.get('agent', None)
        if self._agent is None:
            self._agent = instantiate_from_file(self._config_filepath)

        self._action_order = state.get('action_order', None)
        if self._action_order is None:
            self._action_order = default_action_order

        self._n_actions = self._agent.num_actions
        self._warm_start = state.get('warm_start', self._warm_start)

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

        def preferred_skill_orchestrator_setup(advantage_skill, disadvantage_skill):
            self.__add_to_action_order__(advantage_skill)
            self.__add_to_action_order__(disadvantage_skill)
            profile = 'preferred-skill'
            kwargs = {
                'n_points': 1000,
                'context_size': self._n_actions,
                'advantage_skillidx': self._action_order[advantage_skill],
                'disadvantage_skillidx': self._action_order[disadvantage_skill]
            }
            return profile, kwargs

        try:
            warm_start_methods = {
                'noop': noop_setup,
                'ignore-skill': ignore_skill_setup,
                'max-orchestrator': max_orchestrator_setup,
                'preferred-skill': preferred_skill_orchestrator_setup
            }

            method = warm_start_methods[self._warm_start_type.lower()]
            profile, kwargs = method(**self._warm_start_kwargs)

            tids, contexts, arm_rewards = warm_start_datagen.get_warmstart_data(
                profile, **kwargs
            )

            self._agent.warm_start(tids, arm_rewards, contexts=contexts)
            self._warm_start = False

            self.save()
        except Exception as err:
            logger.warning('Exception in warm starting orchestrator. Error: ' + str(err))
            raise err

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

    def __build_context__(self,
                          candidate_actions: Optional[List[Union[Action, List[Action]]]]
                          ) -> np.array:

        context = [0.0] * self._n_actions

        noop_pos = self._action_order[self.noop_command]
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

        if suggested_agent == self.noop_command or suggested_agent is None:
            return None

        for action in candidate_actions:
            if action.agent_owner == suggested_agent:
                return action

        return None

    def record_transition(self,
                          prev_state: TerminalReplayMemoryComplete,
                          current_state_pre: TerminalReplayMemory):

        try:
            prev_state_pre = prev_state.pre_replay
            prev_state_post = prev_state.post_replay

            if prev_state_pre.command.action_suggested is None or \
                    prev_state_post.command.action_suggested is None or \
                    prev_state_post.command.action_suggested.suggested_command == self.noop_command:
                return

            reward = float(prev_state_post.command.suggested_executed)

            currently_executed_command = current_state_pre.command.command
            all_the_stuff_from_last_execution = \
                prev_state_pre.command.action_suggested.suggested_command + \
                prev_state_pre.command.action_suggested.description + \
                prev_state_post.command.action_suggested.description

            base = set(currently_executed_command.split())
            reference = set(all_the_stuff_from_last_execution.split())

            # check how much of the current commands is contained in the stuff from last time
            match_score = len(base & reference) / len(base)
            reward += float(match_score > self._reward_match_threshold)

            self._agent.observe(prev_state.post_replay.command.command_id, reward)
        except Exception as err:    # pylint: disable=broad-except
            logger.warning(f'Error in record_transition of bandit orchestrator. Error: {err}')
