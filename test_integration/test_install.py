#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

# pylint: disable=invalid-name,no-value-for-parameter,redefined-outer-name
from time import sleep

from pytest_docker_tools import container, build

from clai.tools.docker_utils import execute_cmd
from test_integration.conftest import get_base_path


my_clai_image = build(
    path=get_base_path(),
    dockerfile='./test_integration/docker/centos/Dockerfile.no.install')

my_clai = container(
    image='{my_clai_image.id}',
)

INSTALL_CORRECTLY_MESSAGE = "CLAI has been installed correctly, you will need to restart your shell."
UNINSTALL_CORRECTLY_MESSAGE = "CLAI has been uninstalled correctly, you need restart your shell."


def test_install_should_finish_correctly(my_clai):
    install_output = execute_cmd(my_clai, "sudo ./install.sh --unassisted --demo")
    assert INSTALL_CORRECTLY_MESSAGE in install_output


def test_install_should_modify_correct_startup_files(my_clai):
    execute_cmd(my_clai, "sudo ./install.sh --unassisted --demo")

    files = my_clai.get_files('/root')
    bashrc_output = str(files['root/.bashrc'])
    bash_profile_output = str(files['root/.bash_profile'])

    assert "# CLAI setup" in bashrc_output
    assert "# CLAI setup" in bash_profile_output
    assert "# End CLAI setup" in bashrc_output
    assert "# End CLAI setup" in bash_profile_output


def test_uninstall_should_return_the_correct_uninstall_message(my_clai):
    execute_cmd(my_clai, "sudo ./install.sh --unassisted --demo")
    uninstall_output = execute_cmd(my_clai, "sudo ./uninstall.sh")
    sleep(2)
    print(uninstall_output)
    assert UNINSTALL_CORRECTLY_MESSAGE in uninstall_output


def test_uninstall_should_return_bash_files_to_previous_state(my_clai):
    files = my_clai.get_files('/root')
    bashrc_original = str(files['root/.bashrc'])
    bash_profile_original = str(files['root/.bash_profile'])
    execute_cmd(my_clai, "sudo ./install.sh --unassisted --demo")
    execute_cmd(my_clai, "sudo ./uninstall.sh")
    sleep(2)
    files = my_clai.get_files('/root')
    bashrc_after_uninstall = str(files['root/.bashrc'])
    bash_profile_after_uninstall = str(files['root/.bash_profile'])

    assert bashrc_after_uninstall == bashrc_original
    assert bash_profile_original == bash_profile_after_uninstall
