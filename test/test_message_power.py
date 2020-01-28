#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from test.test_message_handler import create_mock_agent
from test.state_mother import clai_power_state, ANY_COMMAND_MESSAGE, clai_power_disabled_state
from clai.server.agent_datasource import AgentDatasource
from clai.server.message_handler import MessageHandler
from clai.datasource.server_status_datasource import ServerStatusDatasource
from clai.server.command_message import NOOP_COMMAND


def test_should_active_the_power_mode_when_use_the_command_clai_power(mocker):
    mock_agent = create_mock_agent()
    mocker.patch.object(AgentDatasource, 'get_instances', return_value=[mock_agent], autospec=True)
    message_handler = MessageHandler(ServerStatusDatasource(), mock_agent)

    action = message_handler.process_message(clai_power_state())

    assert action.suggested_command == NOOP_COMMAND
    assert action.description == "You have enabled the auto mode"
    assert action.origin_command == 'clai auto'
    assert action.execute
    assert message_handler.server_status_datasource.is_power()


def test_should_desactive_the_power_mode_when_use_the_command_clai_power_disable(mocker):
    mock_agent = create_mock_agent()
    mocker.patch.object(AgentDatasource, 'get_instances', return_value=[mock_agent], autospec=True)
    message_handler = MessageHandler(ServerStatusDatasource(), mock_agent)
    message_handler.server_status_datasource.set_power(True)

    action = message_handler.process_message(clai_power_disabled_state())

    assert action.suggested_command == NOOP_COMMAND
    assert action.description == 'You have enable the manual mode'
    assert not message_handler.server_status_datasource.is_power()


def test_should_not_change_power_variable_when_active_power_mode_and_it_already_active(mocker):
    mock_agent = create_mock_agent()
    mocker.patch.object(AgentDatasource, 'get_instances', return_value=[mock_agent], autospec=True)
    message_handler = MessageHandler(ServerStatusDatasource(), mock_agent)

    message_handler.server_status_datasource.set_power(True)

    action = message_handler.process_message(clai_power_state())

    assert action.suggested_command == NOOP_COMMAND
    assert action.description == "You have the auto mode already enable, use clai manual to deactivate it"
    assert message_handler.server_status_datasource.is_power()


def test_should_not_change_power_variable_when_active_power_mode_and_it_already_disable(mocker):
    mock_agent = create_mock_agent()
    mocker.patch.object(AgentDatasource, 'get_instances', return_value=[mock_agent], autospec=True)
    message_handler = MessageHandler(ServerStatusDatasource(), mock_agent)

    action = message_handler.process_message(clai_power_disabled_state())

    assert action.suggested_command == NOOP_COMMAND
    assert action.description == "You have manual mode already enable, use clai auto to activate it"
    assert not message_handler.server_status_datasource.is_power()


def test_should_have_action_execute_true_when_power_mode_is_active(mocker):
    mock_agent = create_mock_agent()
    mocker.patch.object(AgentDatasource, 'get_instances', return_value=[mock_agent], autospec=True)
    message_handler = MessageHandler(ServerStatusDatasource(), mock_agent)

    message_handler.process_message(clai_power_state())
    action = message_handler.process_message(ANY_COMMAND_MESSAGE)

    assert action.origin_command == ANY_COMMAND_MESSAGE.command
    assert action.execute
