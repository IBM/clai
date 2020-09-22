#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.datasource.config_storage import ConfigStorage
from clai.datasource.stats_tracker import StatsTracker
from clai.server.agent_datasource import AgentDatasource
from clai.server.clai_message_builder import create_message_list, create_error_select
from clai.server.command_message import State, Action
from clai.server.command_runner.clean_input import extract_quoted_agent_name
from clai.server.command_runner.command_runner import CommandRunner, PostCommandRunner
from clai.server.logger import current_logger as logger


# pylint: disable=too-few-public-methods
class ClaiSelectCommandRunner(CommandRunner, PostCommandRunner):
    SELECT_DIRECTIVE = 'clai activate'

    def __init__(self, config_storage: ConfigStorage, agent_datasource: AgentDatasource):
        self.agent_datasource = agent_datasource
        self.config_storage = config_storage
        self.stats_tracker = StatsTracker()

    def execute(self, state: State) -> Action:
        plugin_to_select = state.command.replace(f'{self.SELECT_DIRECTIVE}', '').strip()
        plugin_to_select = extract_quoted_agent_name(plugin_to_select)

        agent_descriptor = self.agent_datasource.get_agent_descriptor(plugin_to_select)

        plugins_config = self.config_storage.read_config(None)

        if not agent_descriptor:
            return create_error_select(plugin_to_select)

        if agent_descriptor and not agent_descriptor.installed:
            logger.info(f'installing dependencies of plugin {agent_descriptor.name}')

            command = f'$CLAI_PATH/fileExist.sh {agent_descriptor.pkg_name} $CLAI_PATH' \
                    f'{" --user" if plugins_config.user_install else ""}'
            action_selected_to_return = Action(
                suggested_command=command,
                execute=True
            )
        else:
            self.select_plugin(plugin_to_select, state)
            action_selected_to_return = Action(suggested_command=":", execute=True)

        action_selected_to_return.origin_command = state.command
        return action_selected_to_return

    def select_plugin(self, plugin_to_select, state):
        selected_plugin = self.agent_datasource.select_plugin(plugin_to_select, state.user_name)
        if selected_plugin:
            self.stats_tracker.log_activate_skills(state.user_name, plugin_to_select)
            plugins_config = self.config_storage.read_config(state.user_name)
            if plugins_config.selected is None:
                plugins_config.selected = [selected_plugin.name]
            else:
                if selected_plugin.name not in plugins_config.selected:
                    plugins_config.selected.append(selected_plugin.name)
            self.config_storage.store_config(plugins_config, state.user_name)

        return create_message_list(
            self.agent_datasource.get_current_plugin_name(state.user_name),
            self.agent_datasource.all_plugins()
        )

    def execute_post(self, state: State) -> Action:
        plugin_to_select = state.command.replace(f'{self.SELECT_DIRECTIVE}', '').strip()
        plugin_to_select = extract_quoted_agent_name(plugin_to_select)

        agent_descriptor = self.agent_datasource.get_agent_descriptor(plugin_to_select)

        if not agent_descriptor:
            return Action()

        if state.result_code == '0':
            self.agent_datasource.mark_plugins_as_installed(plugin_to_select, state.user_name)
            return self.select_plugin(plugin_to_select, state)

        return create_message_list(
            self.agent_datasource.get_current_plugin_name(state.user_name),
            self.agent_datasource.all_plugins()
        )
