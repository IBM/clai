#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os

from clai.server.logger import current_logger as logger
from clai.server.agent_datasource import AgentDatasource
from clai.server.clai_message_builder import create_message_list, create_error_install
from clai.server.command_message import Action, State
from clai.server.command_runner.command_runner import CommandRunner, PostCommandRunner


# pylint: disable=too-few-public-methods
class ClaiInstallCommandRunner(CommandRunner, PostCommandRunner):
    INSTALL_PLUGIN_DIRECTIVE = "clai install"

    def __init__(self, agent_datasource: AgentDatasource):
        self.agent_datasource = agent_datasource

    @staticmethod
    def __move_plugin__(dir_to_install: str) -> Action:

        if dir_to_install.startswith("http") or dir_to_install.startswith("https"):
            cmd = f"cd $CLAI_PATH/clai/server/plugins && curl -O {dir_to_install}"
            return Action(suggested_command=cmd, execute=True)

        if not os.path.exists(dir_to_install) or not os.path.isdir(dir_to_install):
            return create_error_install(dir_to_install)

        plugin_name = dir_to_install.split("/")[-1]
        logger.info(f"installing plugin name {plugin_name}")
        cmd = f"cp -R {dir_to_install} $CLAI_PATH/clai/server/plugins"
        return Action(suggested_command=cmd, execute=True)

    def execute(self, state: State) -> Action:
        dir_to_install = state.command.replace(
            f"{self.INSTALL_PLUGIN_DIRECTIVE}", ""
        ).strip()
        logger.info(f"trying to install ${dir_to_install}")
        return self.__move_plugin__(dir_to_install)

    def execute_post(self, state: State) -> Action:
        if state.result_code == "0" and state.action_suggested.suggested_command != ":":
            return create_message_list(
                self.agent_datasource.get_current_plugin_name(state.user_name),
                self.agent_datasource.all_plugins(),
            )

        return Action()
