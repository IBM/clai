#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from abc import ABC, abstractmethod
from typing import Optional, List, Union
import os
import shutil
import pickle

from clai.server.command_message import NOOP_COMMAND, State, TerminalReplayMemory, Action, BASEDIR, \
    TerminalReplayMemoryComplete


# pylint: disable=too-many-arguments
class Orchestrator(ABC):

    def __init__(self):
        self.orchestrator_name = self.__class__.__name__
        self._save_basedir = os.path.join(BASEDIR, 'saved_orchestrators')
        self._save_dirpath = os.path.join(self._save_basedir, self.orchestrator_name)
        self.noop_command = NOOP_COMMAND

    # pylint: disable=no-self-use
    def get_orchestrator_state(self):
        """Returns the orchestrator state for persistence"""
        return {}

    @abstractmethod
    def choose_action(self, command: State, agent_names: List[str],
                      candidate_actions: Optional[List[Union[Action, List[Action]]]],
                      force_response: bool, pre_post_state: str) -> Optional[Union[Action, List[Action]]]:
        """Choose an action and agent name for CLAI to respond with"""

    def record_transition(self,
                          prev_state: TerminalReplayMemoryComplete,
                          current_state_pre: TerminalReplayMemory) -> None:
        """
        Record terminal state transition to learn user behavior
        :param prev_state: Previous terminal state
        :param current_state_pre: Current terminal state pre-exec state
        :return: None
        """

    def save(self):
        """Save the orchestrator state"""
        return self.__save_orchestrator__()

    def load(self):
        """Load the orchestrator state"""
        return self.__load_saved_orchestrator__()

    def __prepare_state_folder__(self):

        os.makedirs(self._save_dirpath, exist_ok=True)

        for filename in os.listdir(self._save_dirpath):
            filepath = os.path.join(self._save_dirpath, filename)
            try:
                shutil.rmtree(filepath)
            except OSError:
                os.remove(filepath)

    def __save_orchestrator__(self) -> bool:
        """Saves agent state into persisting memory"""
        try:
            state = self.get_orchestrator_state()
            if not state:
                return True

            self.__prepare_state_folder__()

            for var_name, value in state.items():
                with open(f'{self._save_dirpath}/{var_name}.p', 'wb') as file:
                    pickle.dump(value, file)

        # pylint: disable=broad-except
        except Exception:
            return False
        else:
            return True

    def __load_saved_orchestrator__(self) -> dict:

        orchestrator_state = {}

        files = []
        if os.path.exists(self._save_dirpath):
            files = [file for file in os.listdir(self._save_dirpath)
                     if os.path.isfile(os.path.join(self._save_dirpath, file))]

        for filename in files:
            try:
                key = os.path.splitext(filename)[0]  # filename without extension
                with open(os.path.join(self._save_dirpath, filename), 'rb') as file:
                    orchestrator_state[key] = pickle.load(file)
            # pylint: disable=bare-except
            except:
                pass

        return orchestrator_state

    def __del__(self):
        self.save()

    @staticmethod
    def __calculate_confidence__(action_to_calculate: Union[Action, List[Action]]):
        if isinstance(action_to_calculate, Action):
            return action_to_calculate.confidence

        return action_to_calculate[0].confidence
