#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from typing import Dict

from clai.datasource.config_storage import ConfigStorage
from clai.datasource.server_status_datasource import ServerStatusDatasource
from clai.server.agent_datasource import AgentDatasource
from clai.server.agent_runner import AgentRunner
from clai.server.command_runner.agent_command_runner import AgentCommandRunner
from clai.server.command_runner.clai_delegate_to_agent_command_runner import ClaiDelegateToAgentCommandRunner
from clai.server.command_runner.clai_help_command_runner import ClaiHelpCommandRunner
from clai.server.command_runner.clai_install_command_runner import ClaiInstallCommandRunner
from clai.server.command_runner.clai_plugins_command_runner import ClaiPluginsCommandRunner
from clai.server.command_runner.clai_power_command_runner import ClaiPowerCommandRunner
from clai.server.command_runner.clai_power_disable_command_runner import ClaiPowerDisableCommandRunner
from clai.server.command_runner.clai_select_command_runner import ClaiSelectCommandRunner
from clai.server.command_runner.clai_unselect_command_runner import ClaiUnselectCommandRunner
from clai.server.command_runner.command_runner import CommandRunner, PostCommandRunner

CLAI_COMMAND_NAME = "clai"


# pylint: disable=too-few-public-methods
class CommandRunnerFactory:
    def __init__(self,
                 agent_datasource: AgentDatasource,
                 config_storage: ConfigStorage,
                 server_status_datasource: ServerStatusDatasource
                 ):
        self.server_status_datasource = server_status_datasource
        self.clai_commands: Dict[str, CommandRunner] = {
            "skills": ClaiPluginsCommandRunner(agent_datasource),
            "activate": ClaiSelectCommandRunner(config_storage, agent_datasource),
            "deactivate": ClaiUnselectCommandRunner(config_storage, agent_datasource),
            "manual": ClaiPowerDisableCommandRunner(server_status_datasource),
            "auto": ClaiPowerCommandRunner(server_status_datasource),
            "install": ClaiInstallCommandRunner(agent_datasource),
            "help": ClaiHelpCommandRunner()
        }
        self.clai_post_commands: Dict[str, PostCommandRunner] = {
            "activate": ClaiSelectCommandRunner(config_storage, agent_datasource),
            "install": ClaiInstallCommandRunner(agent_datasource)
        }

    def provide_command_runner(self, command: str, selected_agent: AgentRunner) -> CommandRunner:
        if command.startswith(CLAI_COMMAND_NAME):
            clai_command_name = command.replace(CLAI_COMMAND_NAME, "", 1).strip()
            return self.__get_clai_command_runner(clai_command_name, selected_agent)

        return AgentCommandRunner(selected_agent, self.server_status_datasource)

    def provide_post_command_runner(self, command: str, selected_agent: AgentRunner) -> PostCommandRunner:
        if command.startswith(CLAI_COMMAND_NAME):
            clai_command_name = command.replace(CLAI_COMMAND_NAME, "", 1).strip()
            return self.__get_clai_post_command_runner(clai_command_name, selected_agent)

        return AgentCommandRunner(selected_agent, self.server_status_datasource)

    def __get_clai_post_command_runner(self,
                                       clai_command_name: str,
                                       selected_agent: AgentRunner) -> PostCommandRunner:
        clai_post_commands_names = self.clai_post_commands.keys()

        commands_filtered = filter(clai_command_name.startswith, clai_post_commands_names)
        command_found = next(commands_filtered, None)

        if command_found:
            return self.clai_post_commands[command_found]

        return ClaiDelegateToAgentCommandRunner(
            AgentCommandRunner(selected_agent, self.server_status_datasource)
        )

    def __get_clai_command_runner(self, clai_command_name: str, selected_agent: AgentRunner) -> CommandRunner:
        clai_commands_names = self.clai_commands.keys()

        commands_filtered = filter(clai_command_name.startswith, clai_commands_names)
        command_found = next(commands_filtered, None)

        if command_found:
            return self.clai_commands[command_found]

        return ClaiDelegateToAgentCommandRunner(
            AgentCommandRunner(selected_agent, self.server_status_datasource, ignore_threshold=True)
        )
