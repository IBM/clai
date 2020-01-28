#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from abc import ABC, abstractmethod
from typing import Union, List
import pickle
import os
import shutil

from clai.server.command_message import State, Action, BASEDIR


# pylint: disable=too-few-public-methods,bare-except
class Agent(ABC):

    def __init__(self):
        self.agent_name = self.__class__.__name__
        self.ready = False
        self._save_basedir = os.path.join(BASEDIR, 'saved_agents')
        self._save_dirpath = os.path.join(self._save_basedir, self.agent_name)

    def execute(self, state: State) -> Union[Action, List[Action]]:
        try:
            action_to_return = self.get_next_action(state)
        # pylint: disable=broad-except
        except:
            action_to_return = Action()

        if isinstance(action_to_return, list):
            for action in action_to_return:
                action.agent_owner = self.agent_name
        else:
            action_to_return.agent_owner = self.agent_name
        return action_to_return

    # pylint: disable=no-self-use
    def post_execute(self, state: State) -> Action:
        """Provide a post execution"""
        return Action(origin_command=state.command)

    @abstractmethod
    def get_next_action(self, state: State) -> Union[Action, List[Action]]:
        """Provide next action to execute in the bash console"""

    def init_agent(self):
        """Add here all heavy task for initialize the """

    # pylint: disable=no-self-use
    def get_agent_state(self) -> dict:
        """Returns the agent state to be saved for future loading"""
        return {}

    def __prepare_state_folder__(self):

        os.makedirs(self._save_dirpath, exist_ok=True)

        for file in os.listdir(self._save_dirpath):
            path = os.path.join(self._save_dirpath, file)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)

    def save_agent(self) -> bool:
        """Saves agent state into persisting memory"""
        try:
            state = self.get_agent_state()
            if not state:
                return True

            self.__prepare_state_folder__()

            for var_name, var_val in state.items():
                with open('{}/{}.p'.format(self._save_dirpath, var_name), 'wb') as file:
                    pickle.dump(var_val, file)

        # pylint: disable=broad-except
        except Exception:
            return False
        else:
            return True

    def load_saved_state(self) -> dict:

        agent_state = {}

        filenames = []
        if os.path.exists(self._save_dirpath):
            filenames = [file for file in os.listdir(self._save_dirpath)
                         if os.path.isfile(os.path.join(self._save_dirpath, file))]

        for filename in filenames:
            try:
                key = os.path.splitext(filename)[0]        # filename without extension
                with open(os.path.join(self._save_dirpath, filename), 'rb') as file:
                    agent_state[key] = pickle.load(file)
            except:
                pass

        return agent_state

    def extract_name_without_extension(self, filename):
        return os.path.splitext(filename)[0]

    def __del__(self):
        self.save_agent()


class ClaiIdentity(Agent):

    def get_next_action(self, state: State) -> Action:
        return Action(suggested_command=state.command)
