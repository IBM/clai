#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from test.state_mother import (
    CLAI_INSTALL_STATE_FOLDER,
    CLAI_INSTALL_STATE_URL,
    ANY_ROUTE,
    ANY_URL,
)
from clai.server.clai_message_builder import create_error_install
from clai.server.agent_datasource import AgentDatasource
from clai.server.command_runner.clai_install_command_runner import (
    ClaiInstallCommandRunner,
)

PLUGIN_NAME = "example"
CMD_TO_COPY_PLUGIN_FOLDER = (
    f"sudo cp {ANY_ROUTE} $CLAI_PATH/src/server/plugins | "
    f"sh $CLAI_PATH/fileExist.sh {PLUGIN_NAME} $CLAI_PATH"
)
CMD_TO_COPY_URL_PLUGIN = f"cd $CLAI_PATH/src/server/plugins && curl -O {ANY_URL}"


def test_should_return_the_command_to_get_the_plugin_from_url_and_move_it_into_plugin_folder_server():
    agent_datasource = AgentDatasource()
    clai_install_command_runner = ClaiInstallCommandRunner(agent_datasource)
    command_to_execute = clai_install_command_runner.execute(CLAI_INSTALL_STATE_URL)
    dir_to_install = CLAI_INSTALL_STATE_URL.command.replace(
        f'{"clai install"}', ""
    ).strip()

    assert (
        command_to_execute.suggested_command
        == f"cd $CLAI_PATH/clai/server/plugins && curl -O {dir_to_install}"
    )


def test_should_return_the_command_to_get_the_plugin_from_route_and_move_it_into_plugin_folder_server(
    mocker,
):
    mock_exisit = mocker.patch("os.path.exists")
    mock_exisit.return_value = True
    mock_exisit = mocker.patch("os.path.isdir")
    mock_exisit.return_value = True
    agent_datasource = AgentDatasource()
    clai_install_command_runner = ClaiInstallCommandRunner(agent_datasource)
    command_to_execute = clai_install_command_runner.execute(CLAI_INSTALL_STATE_FOLDER)
    dir_to_install = CLAI_INSTALL_STATE_FOLDER.command.replace(
        f'{"clai install"}', ""
    ).strip()

    assert (
        command_to_execute.suggested_command
        == f"cp -R {dir_to_install} $CLAI_PATH/clai/server/plugins"
    )


def test_should_return_the_message_error_when_the_folder_doesnt_exist(mocker):
    mock_exisit = mocker.patch("os.path.exists")
    mock_exisit.return_value = False
    mock_exisit = mocker.patch("os.path.isdir")
    mock_exisit.return_value = False
    agent_datasource = AgentDatasource()
    clai_install_command_runner = ClaiInstallCommandRunner(agent_datasource)
    command_to_execute = clai_install_command_runner.execute(CLAI_INSTALL_STATE_FOLDER)
    dir_to_install = CLAI_INSTALL_STATE_FOLDER.command.replace(
        f'{"clai install"}', ""
    ).strip()

    assert command_to_execute.suggested_command == ":"
    assert (
        command_to_execute.description
        == create_error_install(dir_to_install).description
    )
