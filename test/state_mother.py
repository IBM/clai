#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.server.command_message import State

ANY_ID = '1'
ANY_INPUT_COMMAND = "command"
ANY_NAME = 'any_name'
ANY_ROUTE = './any_folder'
ANY_URL = 'http://ipv4.download.thinkbroadband.com/5MB.zip'


def clai_plugins_state():
    return State(
        command_id=ANY_ID,
        user_name=ANY_NAME,
        command="clai skills"
    )


def clai_power_state():
    return State(
        command_id=ANY_ID,
        user_name=ANY_NAME,
        command="clai auto"
    )


def clai_power_disabled_state():
    return State(
        command_id=ANY_ID,
        user_name=ANY_NAME,
        command="clai manual"
    )


ANY_COMMAND_MESSAGE = State(
    command_id=ANY_ID,
    user_name=ANY_NAME,
    command=ANY_INPUT_COMMAND
)


def command_state():
    return State(
        command_id=ANY_ID,
        user_name=ANY_NAME,
        command="command"
    )


COMMAND_AGENT_STATE = State(
    command_id=ANY_ID,
    user_name=ANY_NAME,
    command="clai command"
)

COMMAND_NAME_AGENT_STATE = State(
    command_id=ANY_ID,
    user_name=ANY_NAME,
    command='clai "demo agent" command'
)

CLAI_INSTALL_STATE_FOLDER = State(
    command_id=ANY_ID,
    user_name=ANY_NAME,
    command=f"clai install {ANY_ROUTE}"
)

CLAI_INSTALL_STATE_URL = State(
    command_id=ANY_ID,
    user_name=ANY_NAME,
    command=f"clai install {ANY_URL}"
)


def clai_select_state(plugin_to_select):
    return State(
        command_id=ANY_ID,
        user_name=ANY_NAME,
        command=f"clai activate {plugin_to_select}"
    )


def clai_unselect_state(plugin_to_select):
    return State(
        command_id=ANY_ID,
        user_name=ANY_NAME,
        command=f"clai unselect {plugin_to_select}"
    )
