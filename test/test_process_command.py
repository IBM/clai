#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import socket

from test.io_utils import spy_print, mock_input_console
import pytest
from clai.server.socket_client_connector import SocketClientConnector
from clai.server.client_connector import ClientConnector

from clai.process_command import process_command_from_user, COMMAND_START_SERVER, process_command, \
    START_SERVER_COMMAND_TO_EXECUTE
from clai.server.clai_client import ClaiClient, send_command
from clai.server.command_message import Action

ANY_INPUT_COMMAND = "command"
ANY_NO_ACTION = Action(origin_command="command", suggested_command="command")
SUGGESTED_ACTION = Action(origin_command="command", suggested_command="suggested_command")
EXECUTABLE_ACTION = Action(origin_command="command", suggested_command="suggested_command", execute=True)
BASIC_ACTION = Action(origin_command="command")
ANY_ID = '1'
ANY_USER = 'any_user'


def test_should_return_any_action_when_everything_works_correctly(mocker):
    mocker.patch.object(ClaiClient, 'send', return_value=ANY_NO_ACTION, autospec=True)
    action = send_command(ANY_ID, ANY_USER, ANY_NO_ACTION.origin_command)

    assert action == ANY_NO_ACTION


def test_should_return_a_valid_action_when_socket_crash(mocker):
    mocker.patch.object(SocketClientConnector, 'send', side_effect=socket.error(), autospec=True)

    action = send_command(ANY_ID, ANY_USER, ANY_NO_ACTION.origin_command)

    assert action == ANY_NO_ACTION


def test_should_return_the_original_command_when_read_throw_exception(mocker):
    mocker.patch.object(ClientConnector, 'send', side_effect=socket.error(), autospec=True)

    command_to_execute, _ = process_command_from_user(ANY_ID, ANY_USER, ANY_INPUT_COMMAND)

    assert command_to_execute == ANY_INPUT_COMMAND


def test_should_not_print_the_suggested_dialog_when_suggested_is_the_same(mocker):
    spy_print(mocker)
    mocker.patch.object(ClaiClient, 'send', return_value=ANY_NO_ACTION, autospec=True)

    process_command_from_user(ANY_ID, ANY_USER, ANY_NO_ACTION.origin_command)

    # pylint: disable=no-member
    assert print.call_count == 0


def test_should_print_the_suggested_dialog_when_suggested_is_different(mocker):
    spy_print(mocker)
    mock_input_console(mocker, 'n')
    mocker.patch.object(ClaiClient, 'send', return_value=SUGGESTED_ACTION, autospec=True)

    process_command_from_user(ANY_ID, ANY_USER, ANY_INPUT_COMMAND)

    # pylint: disable=no-member
    assert print.call_count == 1


def test_should_not_print_the_suggested_dialog_when_suggested_is_different_and_execute_is_enable(mocker):
    spy_print(mocker)
    mocker.patch.object(ClaiClient, 'send', return_value=EXECUTABLE_ACTION, autospec=True)

    process_command_from_user(ANY_ID, ANY_USER, ANY_NO_ACTION.origin_command)

    # pylint: disable=no-member
    assert print.call_count == 0


def test_should_not_print_the_suggested_dialog_when_the_action_only_contains_original_command(mocker):
    spy_print(mocker)
    mocker.patch.object(ClaiClient, 'send', return_value=BASIC_ACTION, autospec=True)

    process_command_from_user(ANY_ID, ANY_USER, ANY_INPUT_COMMAND)

    # pylint: disable=no-member
    assert print.call_count == 0


def test_should_not_print_the_suggested_dialog_when_suggested_command_is_empty(mocker):
    spy_print(mocker)
    empty_suggested_command = Action(origin_command=ANY_INPUT_COMMAND, suggested_command="")
    mocker.patch.object(ClaiClient, 'send', return_value=empty_suggested_command, autospec=True)

    process_command_from_user(ANY_ID, ANY_USER, ANY_INPUT_COMMAND)

    # pylint: disable=no-member
    assert print.call_count == 0


def test_should_return_the_original_command_when_the_command_is_the_same(mocker):
    mocker.patch.object(ClaiClient, 'send', return_value=ANY_NO_ACTION, autospec=True)

    command_to_execute, _ = process_command_from_user(ANY_ID, ANY_USER, ANY_NO_ACTION.origin_command)

    assert command_to_execute == ANY_NO_ACTION.origin_command


def test_should_return_the_suggested_command_when_the_user_press_yes(mocker):
    mock_input_console(mocker, 'y')
    mocker.patch.object(ClaiClient, 'send', return_value=SUGGESTED_ACTION, autospec=True)

    command_to_execute, _ = process_command_from_user(ANY_ID, ANY_USER, SUGGESTED_ACTION.origin_command)

    assert command_to_execute == SUGGESTED_ACTION.suggested_command


def test_should_return_the_original_command_when_the_user_press_no(mocker):
    mock_input_console(mocker, 'n')
    mocker.patch.object(ClaiClient, 'send', return_value=SUGGESTED_ACTION, autospec=True)

    command_to_execute, _ = process_command_from_user(ANY_ID, ANY_USER, SUGGESTED_ACTION.origin_command)

    assert command_to_execute == SUGGESTED_ACTION.origin_command


def test_should_return_the_suggested_command_when_the_action_execute_true(mocker):
    mocker.patch.object(ClaiClient, 'send', return_value=EXECUTABLE_ACTION, autospec=True)

    command_to_execute, _ = process_command_from_user(ANY_ID, ANY_USER, EXECUTABLE_ACTION.origin_command)

    assert command_to_execute == EXECUTABLE_ACTION.suggested_command


def test_should_return_the_original_command_when_the_action_not_contains_suggestion(mocker):
    mocker.patch.object(ClaiClient, 'send', return_value=BASIC_ACTION, autospec=True)

    command_to_execute, _ = process_command_from_user(ANY_ID, ANY_USER, BASIC_ACTION.origin_command)

    assert command_to_execute == BASIC_ACTION.origin_command


def test_should_return_the_start_server_command_when_received_clai_start(mocker):
    with pytest.raises(SystemExit):
        mock_override_last_command = mocker.patch('clai.process_command.override_last_command')

        process_command(ANY_ID, ANY_USER, COMMAND_START_SERVER)

        mock_override_last_command.assert_called_once_with(f"\n{START_SERVER_COMMAND_TO_EXECUTE}\n")
