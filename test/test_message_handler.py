#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from unittest import mock
from unittest.mock import Mock

from test.mock_executor import MockExecutor
from test.state_mother import clai_plugins_state, clai_select_state, command_state, COMMAND_AGENT_STATE, \
    COMMAND_NAME_AGENT_STATE
import pytest
from clai.server.message_handler import MessageHandler
from clai.datasource.server_status_datasource import ServerStatusDatasource
from clai.server.clai_message_builder import create_error_select
from clai.server.command_runner.agent_descriptor import AgentDescriptor
from clai.datasource.config_storage import ConfigStorage
from clai.datasource.model.plugin_config import PluginConfig
from clai.server.agent import Agent
from clai.server.agent_datasource import AgentDatasource
from clai.server.command_message import Action, NOOP_COMMAND
from clai.tools.colorize_console import Colorize

NO_SELECTED = PluginConfig(default_orchestrator="max_orchestrator")
ALL_PLUGINS = [AgentDescriptor(pkg_name="demo_agent", name="demo_agent"),
               AgentDescriptor(pkg_name="nlc2cmd", name="nlc2cmd")]

ALL_PLUGINS_WITH_TAR_INSTALLED = [
    AgentDescriptor(pkg_name="demo_agent", name="demo_agent", installed=True),
    AgentDescriptor(pkg_name="nlc2cmd", name="nlc2cmd", installed=True)]


def get_printable_name(plugin: AgentDescriptor):
    composed_name = f"{plugin.name} "
    if plugin.installed:
        composed_name = composed_name + "(Installed)"
    else:
        composed_name = composed_name + "(Not Installed)"

    return composed_name


def expected_description(all_plugins, selected) -> str:
    text = 'Available Skills:\n'

    for plugin in all_plugins:
        if plugin.pkg_name in selected:
            text += Colorize().emoji(Colorize.EMOJI_CHECK).complete() \
                .append(f" {get_printable_name(plugin)}\n") \
                .to_console()

        else:
            text += Colorize().emoji(Colorize.EMOJI_BOX) \
                .append(f' {get_printable_name(plugin)}\n') \
                .to_console()

    return text


def create_mock_agent() -> Agent:
    agent = Mock(spec=Agent)
    agent.agent_name = "demo_agent"
    return agent


@pytest.yield_fixture(scope='session', autouse=True)
def mock_executor():
    with mock.patch('clai.server.agent_runner.agent_executor', MockExecutor()) as _fixture:
        yield _fixture


def test_should_return_the_list_of_plugins_with_default_selected_when_the_server_received_plugins_no_selected(mocker):
    mock_agent = create_mock_agent()
    mocker.patch.object(AgentDatasource, 'get_instances', return_value=[mock_agent], autospec=True)
    mocker.patch.object(ConfigStorage, 'read_config', return_value=NO_SELECTED, autospec=True)
    mocker.patch.object(AgentDatasource, 'all_plugins', return_value=ALL_PLUGINS, autospec=True)
    message_handler = MessageHandler(ServerStatusDatasource(), AgentDatasource())

    action = message_handler.process_message(clai_plugins_state())

    assert action.suggested_command == NOOP_COMMAND
    assert action.origin_command == 'clai skills'
    assert action.execute
    assert action.description == expected_description(ALL_PLUGINS, NO_SELECTED.default)


def test_should_return_the_list_of_plugins_with_selected_when_the_server_received_plugins(mocker):
    mock_agent = create_mock_agent()
    mocker.patch.object(AgentDatasource, 'get_instances', return_value=[mock_agent], autospec=True)
    agent_selected = 'nlc2cmd'
    mocker.patch.object(AgentDatasource, 'all_plugins', return_value=ALL_PLUGINS, autospec=True)
    mocker.patch.object(ConfigStorage, 'read_all_user_config', return_value=None, autospec=True)
    mocker.patch.object(
        ConfigStorage, 'read_config', return_value=PluginConfig(
            selected=[agent_selected], default_orchestrator="max_orchestrator"), autospec=True)
    message_handler = MessageHandler(ServerStatusDatasource(), AgentDatasource())

    action = message_handler.process_message(clai_plugins_state())

    assert action.suggested_command == NOOP_COMMAND
    assert action.origin_command == 'clai skills'
    assert action.execute
    assert action.description == expected_description(ALL_PLUGINS, agent_selected)


def test_should_return_the_list_without_any_selected_plugin_when_default_doesnt_exist(mocker):
    mock_agent = create_mock_agent()
    mocker.patch.object(AgentDatasource, 'get_instances', return_value=[mock_agent], autospec=True)
    mocker.patch.object(AgentDatasource, 'all_plugins', return_value=ALL_PLUGINS, autospec=True)
    mocker.patch.object(ConfigStorage, 'read_config', return_value=PluginConfig(
        default="", default_orchestrator="max_orchestrator"), autospec=True)
    message_handler = MessageHandler(ServerStatusDatasource(), AgentDatasource())

    action = message_handler.process_message(clai_plugins_state())

    assert action.suggested_command == NOOP_COMMAND
    assert action.origin_command == 'clai skills'
    assert action.execute
    assert action.description == expected_description(ALL_PLUGINS, '')


def test_should_return_the_install_command_when_the_new_plugin_is_not_installed_yet(mocker):
    mock_agent = create_mock_agent()
    mocker.patch.object(AgentDatasource, 'get_instances', return_value=[mock_agent], autospec=True)
    mocker.patch.object(ConfigStorage, 'read_config', return_value=PluginConfig(
        selected=["nlc2cmd"], default_orchestrator="max_orchestrator"), autospec=True)
    mocker.patch.object(ConfigStorage, 'store_config', return_value=None, autospec=True)
    mocker.patch.object(AgentDatasource, 'all_plugins', return_value=ALL_PLUGINS, autospec=True)
    message_handler = MessageHandler(ServerStatusDatasource(), AgentDatasource())

    select_agent = clai_select_state('nlc2cmd')
    action = message_handler.process_message(select_agent)

    assert action.suggested_command == "$CLAI_PATH/fileExist.sh nlc2cmd --path $CLAI_PATH"
    assert action.origin_command == select_agent.command
    assert message_handler.agent_datasource.get_current_plugin_name(select_agent.user_name) == ['nlc2cmd']


def test_should_return_the_list_with_the_new_selected_values_if_exists_and_is_installed(mocker):
    mock_agent = create_mock_agent()
    mocker.patch.object(AgentDatasource, 'get_instances', return_value=[mock_agent], autospec=True)
    mocker.patch.object(ConfigStorage, 'read_config', return_value=PluginConfig(
        selected=["demo_agent"], default_orchestrator="max_orchestrator"), autospec=True)
    mocker.patch.object(ConfigStorage, 'store_config', return_value=None, autospec=True)
    mocker.patch.object(AgentDatasource, 'all_plugins', return_value=ALL_PLUGINS_WITH_TAR_INSTALLED, autospec=True)
    message_handler = MessageHandler(ServerStatusDatasource(), AgentDatasource())

    select_agent = clai_select_state('nlc2cmd')
    action = message_handler.process_message(select_agent)

    assert action.suggested_command == NOOP_COMMAND
    assert action.origin_command == select_agent.command
    assert action.execute
    assert message_handler.agent_datasource.get_current_plugin_name(select_agent.user_name) == ['nlc2cmd']


def test_should_return_an_error_when_agent_doesnt_exist(mocker):
    mock_agent = create_mock_agent()
    mocker.patch.object(AgentDatasource, 'get_instances', return_value=[mock_agent], autospec=True)
    mocker.patch.object(AgentDatasource, 'all_plugins', return_value=ALL_PLUGINS, autospec=True)
    mocker.patch.object(ConfigStorage, 'read_config', return_value=PluginConfig(
        selected=["nlc2cmd"], default_orchestrator="max_orchestrator"), autospec=True)
    mocker.patch.object(ConfigStorage, 'store_config', return_value=None, autospec=True)
    message_handler = MessageHandler(ServerStatusDatasource(), AgentDatasource())

    select_agent = clai_select_state('wrong_agent')
    action = message_handler.process_message(select_agent)

    assert action.suggested_command == NOOP_COMMAND
    assert action.origin_command == select_agent.command
    assert action.execute
    assert action.description == create_error_select('wrong_agent').description
    assert message_handler.agent_datasource.get_current_plugin_name(select_agent.user_name) == ['nlc2cmd']


def test_should_return_an_error_when_selected_is_empty(mocker):
    mock_agent = create_mock_agent()
    mocker.patch.object(AgentDatasource, 'get_instances', return_value=[mock_agent], autospec=True)
    mocker.patch.object(AgentDatasource, 'all_plugins', return_value=ALL_PLUGINS, autospec=True)
    mocker.patch.object(ConfigStorage, 'read_config', return_value=PluginConfig(
        selected=["nlc2cmd"], default_orchestrator="max_orchestrator"), autospec=True)
    mocker.patch.object(ConfigStorage, 'store_config', return_value=None, autospec=True)
    message_handler = MessageHandler(ServerStatusDatasource(), AgentDatasource())

    select_agent = clai_select_state('')
    action = message_handler.process_message(select_agent)

    assert action.suggested_command == NOOP_COMMAND
    assert action.origin_command == select_agent.command
    assert action.execute
    assert action.description == create_error_select('').description
    assert message_handler.agent_datasource.get_current_plugin_name(select_agent.user_name) == ['nlc2cmd']


# @patch('clai.server.agent_executor.thread_executor', MockExecutor())
def test_should_return_the_action_from_selected_agent_when_the_command_goes_to_the_agent_and_threshold_is_ok(mocker):
    mock_agent = create_mock_agent()
    mocker.patch.object(AgentDatasource, 'get_instances', return_value=[mock_agent], autospec=True)
    action_to_execute = Action(suggested_command="command", confidence=1.0)
    mock_agent.execute.return_value = action_to_execute
    mocker.patch.object(ConfigStorage, 'read_config', return_value=PluginConfig(
        selected=["demo_agent"], default_orchestrator="max_orchestrator"), autospec=True)
    message_handler = MessageHandler(ServerStatusDatasource(), AgentDatasource())

    action = message_handler.process_message(command_state())

    assert action.suggested_command == action_to_execute.suggested_command
    assert action.origin_command == command_state().command
    assert not action.execute
    assert not action.description


# @patch('clai.server.agent_executor.thread_executor', MockExecutor())
def test_should_return_empty_action_from_selected_agent_when_the_command_goes_to_the_agent_and_not_confidence(mocker):
    mock_agent = create_mock_agent()
    mocker.patch.object(AgentDatasource, 'get_instances', return_value=[mock_agent], autospec=True)
    action_to_execute = Action(suggested_command="command", confidence=0.1)
    mock_agent.execute.return_value = action_to_execute
    mocker.patch.object(ConfigStorage, 'read_config', return_value=PluginConfig(
        selected=["demo_agent"], default_orchestrator="max_orchestrator"), autospec=True)
    message_handler = MessageHandler(ServerStatusDatasource(), AgentDatasource())

    action = message_handler.process_message(command_state())

    assert action.suggested_command is action.origin_command
    assert action.origin_command == command_state().command
    assert not action.execute
    assert not action.description


# @patch('clai.server.agent_executor.thread_executor', MockExecutor())
def test_should_return_the_suggestion_from_agent_ignoring_confidence_if_is_clai_command(mocker):
    mock_agent = create_mock_agent()
    mocker.patch.object(AgentDatasource, 'get_instances', return_value=[mock_agent], autospec=True)
    action_to_execute = Action(suggested_command="command", confidence=0.0)
    mock_agent.execute.return_value = action_to_execute
    mocker.patch.object(ConfigStorage, 'read_config', return_value=PluginConfig(
        selected=["demo_agent"], default_orchestrator="max_orchestrator"), autospec=True)
    message_handler = MessageHandler(ServerStatusDatasource(), AgentDatasource())

    action = message_handler.process_message(COMMAND_AGENT_STATE)

    assert action.suggested_command == action_to_execute.suggested_command
    assert action.origin_command == command_state().command
    assert not action.execute
    assert not action.description


# @patch('clai.server.agent_executor.thread_executor', MockExecutor())
def test_should_return_the_suggestion_from_agent_ignoring_confidence_if_is_name_agent_command(mocker):
    mock_agent = create_mock_agent()
    mocker.patch.object(AgentDatasource, 'get_instances', return_value=[mock_agent], autospec=True)
    action_to_execute = Action(suggested_command="command", confidence=0.0)
    mock_agent.execute.return_value = action_to_execute
    mocker.patch.object(ConfigStorage, 'read_config', return_value=PluginConfig(
        selected=["demo_agent"], default_orchestrator="max_orchestrator"), autospec=True)
    message_handler = MessageHandler(ServerStatusDatasource(), AgentDatasource())

    action = message_handler.process_message(COMMAND_NAME_AGENT_STATE)

    assert action.suggested_command == action_to_execute.suggested_command
    assert action.origin_command == command_state().command
    assert not action.execute
    assert not action.description


def test_should_return_valid_action_if_the_select_agent_return_none(mocker):
    mock_agent = create_mock_agent()
    mocker.patch.object(AgentDatasource, 'get_instances', return_value=[mock_agent], autospec=True)
    mock_agent.execute.return_value = None
    mocker.patch.object(ConfigStorage, 'read_config', return_value=PluginConfig(
        selected=["demo_agent"], default_orchestrator="max_orchestrator"), autospec=True)
    message_handler = MessageHandler(ServerStatusDatasource(), AgentDatasource())

    action = message_handler.process_message(command_state())

    assert action.suggested_command is action.origin_command
    assert action.origin_command == command_state().command
    assert not action.execute
    assert not action.description
