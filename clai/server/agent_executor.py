#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from abc import ABC, abstractmethod
from concurrent import futures
from functools import partial
from operator import is_not
from typing import List, Union

from clai.server.agent import Agent
from clai.server.command_message import Action, State


# pylint: disable=too-few-public-methods
class AgentExecutor(ABC):
    @abstractmethod
    def execute_agents(self, command: State, agents: List[Agent]) -> List[Action]:
        """execute all agents in parallel and return the actions"""


class ThreadExecutor(AgentExecutor):
    MAX_TIME_PLUGIN_EXECUTION = 4
    NUM_WORKERS = 4

    def execute_agents(
        self, command: State, agents: List[Agent]
    ) -> List[Union[Action, List[Action]]]:
        with futures.ThreadPoolExecutor(max_workers=self.NUM_WORKERS) as executor:
            done, _ = futures.wait(
                [
                    executor.submit(plugin_instance.execute, command)
                    for plugin_instance in agents
                ],
                timeout=self.MAX_TIME_PLUGIN_EXECUTION,
            )
            if not done:
                return []
            results = map(lambda future: future.result(), done)
            candidate_actions = list(filter(partial(is_not, None), results))
        return candidate_actions


# pylint: disable= invalid-name
thread_executor = ThreadExecutor()
