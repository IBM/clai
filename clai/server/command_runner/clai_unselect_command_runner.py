#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.datasource.config_storage import ConfigStorage
from clai.datasource.stats_tracker import StatsTracker
from clai.server.agent_datasource import AgentDatasource
from clai.server.clai_message_builder import create_message_list
from clai.server.command_message import State, Action
from clai.server.command_runner.clean_input import extract_quoted_agent_name
from clai.server.command_runner.command_runner import CommandRunner


# pylint: disable=too-few-public-methods
class ClaiUnselectCommandRunner(CommandRunner):
    UNSELECT_DIRECTIVE = 'clai deactivate'

    def __init__(self, config_storage: ConfigStorage, agent_datasource: AgentDatasource):
        self.config_storage = config_storage
        self.agent_datasource = agent_datasource
        self.stats_tracker = StatsTracker()

    def execute(self, state: State) -> Action:
        plugin_to_select = state.command.replace(f'{self.UNSELECT_DIRECTIVE}', '').strip()

        plugin_to_select = extract_quoted_agent_name(plugin_to_select)

        selected = self.agent_datasource.unselect_plugin(plugin_to_select, state.user_name)
        if selected:
            self.stats_tracker.log_deactivate_skills(state.user_name, plugin_to_select)
            plugins_config = self.config_storage.read_config(state.user_name)
            if plugins_config.selected is not None and selected.name in plugins_config.selected:
                plugins_config.selected.remove(selected.name)
            self.config_storage.store_config(plugins_config, state.user_name)

        action_to_return = create_message_list(
            self.agent_datasource.get_current_plugin_name(state.user_name),
            self.agent_datasource.all_plugins()
        )
        action_to_return.origin_command = state.command
        return action_to_return
