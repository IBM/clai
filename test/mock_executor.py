#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from typing import List

from clai.server.agent import Agent
from clai.server.agent_datasource_executor import AgentDatasourceExecutor
from clai.server.agent_executor import AgentExecutor
from clai.server.command_message import State, Action


# pylint: disable=too-few-public-methods
class MockExecutor(AgentExecutor):
    def execute_agents(self, command: State, agents: List[Agent]) -> List[Action]:
        return list(map(lambda agent: self.execute(command, agent), agents))

    @staticmethod
    def execute(command: State, agent: Agent) -> Action:
        action = agent.execute(command)
        if not action:
            action = Action()
        return action


class MockAgentDatasourceExecutor(AgentDatasourceExecutor):
    def execute(self, load_agent, pkg_name):
        load_agent(pkg_name)
