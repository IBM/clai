#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

# pylint: disable=invalid-name,no-value-for-parameter
import os

from pytest_docker_tools import build, container


def get_base_path():
    root_path = os.getcwd()
    print(root_path)
    if 'test_integration' in root_path:
        return '../'

    return '.'


my_clai_installed_image = build(
    path=get_base_path(),
    dockerfile='./test_integration/docker/centos/Dockerfile',
    rm=True
)

my_clai_module = container(
    image='{my_clai_installed_image.id}',
    scope='module'
)


def pytest_generate_tests(metafunc):
    if "command" in metafunc.fixturenames:
        commands = getattr(metafunc.cls, 'get_commands_to_execute')(metafunc.cls)
        commands_expected = getattr(metafunc.cls, 'get_commands_expected')(metafunc.cls)
        metafunc.parametrize(["command", 'command_expected'], list(zip(commands, commands_expected)))
