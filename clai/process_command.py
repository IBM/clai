#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import io
import sys

from typing import Optional

from clai.server.clai_client import send_command
from clai.server.clai_message_builder import create_message_help, create_message_server_runing
from clai.server.command_message import Action, NOOP_COMMAND
from clai.server.message_handler import STOP_COMMAND
from clai.tools.colorize_console import Colorize
from clai.tools.file_util import get_history_file_name, read_history

COMMAND_START_SERVER = 'clai start'
COMMAND_BASE = 'clai'

START_SERVER_COMMAND_TO_EXECUTE = 'nohup $CLAI_PATH/bin/clai-run start &'


def override_last_command(last_command):
    lines = read_history()

    new_last_line = (lines[-1].rstrip() + last_command)
    lines[-1] = new_last_line

    io.open(get_history_file_name(), 'w').writelines(lines)


def is_yes_command(input_command):
    return input_command in ('y', 'yes')


def is_not_command(input_command):
    return input_command in ('n', 'no')


def is_explain_command(input_command):
    return input_command in ('e', 'explain')


def ask_user_prompt(command_to_execute: Action) -> Optional[str]:
    if command_to_execute.is_same_command():
        return command_to_execute.origin_command

    if command_to_execute.execute:
        return command_to_execute.suggested_command

    print(Colorize()
          .emoji(Colorize.EMOJI_ROBOT)
          .info()
          .append("  Suggests: ")
          .info()
          .append(f"{command_to_execute.suggested_command} ")
          .append("(y/n/e)")
          .to_console())

    while True:
        command_input = input()
        if is_yes_command(command_input):
            return command_to_execute.suggested_command

        if is_not_command(command_input):
            return command_to_execute.origin_command

        if is_explain_command(command_input):
            print(Colorize().warning().append(f"Description: {command_to_execute.description}").to_console())

        print(Colorize()
              .info()
              .append('choose yes[y] or no[n] or explain[e]')
              .to_console())


def process_command_from_user(command_id, user_name, command_to_check):
    command_to_execute = send_command(command_id=command_id, user_name=user_name, command_to_check=command_to_check)

    if command_to_execute.origin_command == STOP_COMMAND:
        print(Colorize()
              .info()
              .append("Clai has been stopped")
              .to_console())
        return NOOP_COMMAND, False

    if command_to_execute.description and command_to_execute.suggested_command == ":":
        print(command_to_execute.description)

    command_accepted_by_the_user = ask_user_prompt(command_to_execute)

    return command_accepted_by_the_user, command_to_execute.pending_actions


def process_command(command_id, user_name, command_to_check):
    pending_commands = False

    if command_to_check == COMMAND_START_SERVER:
        command_accepted_by_the_user = START_SERVER_COMMAND_TO_EXECUTE
        print(Colorize()
              .info()
              .append("CLAI Starting. CLAI could take a while to start replying")
              .to_console())
    elif command_to_check.strip() == COMMAND_BASE.strip():
        command_accepted_by_the_user = NOOP_COMMAND
        print(create_message_server_runing())
        print(create_message_help().description)
    else:
        command_accepted_by_the_user, pending_commands = \
            process_command_from_user(command_id, user_name, command_to_check)

    override_last_command("\n" + command_accepted_by_the_user + "\n")

    if not pending_commands:
        sys.exit(1)
