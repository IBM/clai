#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from typing import Optional, List, Union

from clai.datasource.action_remote_storage import ActionRemoteStorage
from clai.server.agent_datasource import AgentDatasource
from clai.server.command_message import State, Action, TerminalReplayMemory
from clai.server.agent import Agent
from clai.server.agent_executor import thread_executor as agent_executor
from clai.server.orchestration.orchestrator_provider import OrchestratorProvider
from clai.server.orchestration.orchestrator_storage import OrchestratorStorage


class AgentRunner:
    def __init__(self, agent_datasource: AgentDatasource,
                 orchestrator_provider: OrchestratorProvider
                 ):

        self.agent_datasource = agent_datasource
        self.orchestrator_provider = orchestrator_provider
        self.remote_storage = ActionRemoteStorage()
        self.orchestrator_storage = OrchestratorStorage(orchestrator_provider, self.remote_storage)

        self._pre_exec_id = "pre"
        self._post_exec_id = "post"

    # pylint: disable=too-many-arguments
    def store_pre_orchestrator_memory(self,
                                      command: State,
                                      agent_list: List[Agent],
                                      candidate_actions: Optional[List[Union[Action, List[Action]]]],
                                      force_response: bool,
                                      suggested_command: Optional[Action]):

        agent_names = [agent.agent_name for agent in agent_list]
        state = TerminalReplayMemory(command, agent_names, candidate_actions,
                                     force_response, suggested_command)
        self.orchestrator_storage.store_pre(state)

    # pylint: disable=too-many-arguments
    def store_post_orchestrator_memory(self,
                                       command: State,
                                       agent_list: List[Agent],
                                       candidate_actions: Optional[List[Union[Action, List[Action]]]],
                                       force_response: bool,
                                       suggested_command: Optional[Action]):

        agent_names = [agent.agent_name for agent in agent_list]
        state = TerminalReplayMemory(command, agent_names, candidate_actions,
                                     force_response, suggested_command)
        self.orchestrator_storage.store_post(state)

    # pylint: disable=too-many-arguments
    def select_best_candidate(self, command: State, agent_list: List[Agent],
                              candidate_actions: Optional[List[Union[Action, List[Action]]]],
                              force_response: bool, pre_post_state: str) -> Optional[Union[Action, List[Action]]]:
        agent_names = [agent.agent_name for agent in agent_list]

        orchestrator = self.orchestrator_provider.get_current_orchestrator()
        suggested_command = orchestrator.choose_action(
            command=command, agent_names=agent_names, candidate_actions=candidate_actions,
            force_response=force_response, pre_post_state=pre_post_state)

        if not suggested_command:
            suggested_command = Action()

        return suggested_command

    def process(self,
                command: State,
                ignore_threshold: bool,
                force_agent: str = None) -> Optional[Union[Action, List[Action]]]:
        if force_agent:
            plugin_instances = self.agent_datasource.get_instances(command.user_name, force_agent)
            ignore_threshold = True
        else:
            plugin_instances = self.agent_datasource.get_instances(command.user_name)

        candidate_actions = agent_executor.execute_agents(command, plugin_instances)

        suggested_command = self.select_best_candidate(command, plugin_instances, candidate_actions,
                                                       ignore_threshold, self._pre_exec_id)

        if not suggested_command:
            suggested_command = Action()

        self.store_pre_orchestrator_memory(command, plugin_instances, candidate_actions, ignore_threshold,
                                           suggested_command)

        if isinstance(suggested_command, Action):
            if not suggested_command.suggested_command:
                suggested_command.suggested_command = command.command
        else:
            for action in suggested_command:
                if not action.suggested_command:
                    action.suggested_command = command.command

        return suggested_command

    def process_post(self, command: State, ignore_threshold: bool) -> Optional[Action]:
        plugin_instances = self.agent_datasource.get_instances(command.user_name)
        candidate_actions = []
        for plugin_instance in plugin_instances:
            action_post_executed = plugin_instance.post_execute(command)
            action_post_executed.agent_owner = plugin_instance.agent_name
            if action_post_executed:
                candidate_actions.append(action_post_executed)

        suggested_command = self.select_best_candidate(command, plugin_instances, candidate_actions,
                                                       ignore_threshold, self._post_exec_id)

        self.store_post_orchestrator_memory(command, plugin_instances, candidate_actions, ignore_threshold,
                                            suggested_command)

        if not suggested_command:
            suggested_command = Action()

        if not suggested_command.suggested_command:
            suggested_command.suggested_command = command.command

        return suggested_command
