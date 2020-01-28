#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os
import subprocess
import sys
import threading
from typing import Optional

import docker
from pytest_docker_tools.utils import wait_for_callable
from pytest_docker_tools.wrappers import Container

from clai.server.agent_datasource import AgentDatasource
from clai.server.clai_client import send_command
from clai.server.command_message import Action

# pylint: disable=too-many-instance-attributes
from clai.tools.docker_utils import execute_cmd


class EmulatorPresenter:
    def __init__(self, on_skills_ready, on_server_running, on_server_stopped):
        self.server_running = False
        self.server_process = None
        self.current_active_skill = ''
        self.agent_datasource = AgentDatasource()

        self.on_skills_ready = on_skills_ready
        self.on_server_running = on_server_running
        self.on_server_stopped = on_server_stopped

        self.my_clai: Optional[Container] = None

    @staticmethod
    def __get_base_path():
        root_path = os.getcwd()
        print(f"the path {root_path}")
        if 'bin' in root_path:
            return '../'

        return '.'

    def stop_server(self):
        if self.server_process:
            self.server_process.kill()

    def select_skill(self, skill_name: str):
        if skill_name == self.current_active_skill:
            return

        self._send_select(skill_name)
        self._send_unselect(self.current_active_skill)

        self.request_skills()

    def request_skills(self):
        response = execute_cmd(self.my_clai, "clai skills")

        skills_as_string = response
        skills_as_array = skills_as_string.splitlines()
        self.on_skills_ready(skills_as_array[2:-1])

    def send_message(self, message):

        response = self._send_to_emulator(message)
        print(response)

        return response

    def _send_select(self, skill_name: str):
        self._send_to_emulator(f'clai select {skill_name}')

    def _send_unselect(self, skill_name: str):
        self._send_to_emulator(f'clai unselect {skill_name}')

    def _send_to_emulator(self, command: str) -> str:
        response = execute_cmd(self.my_clai, command)

        return response

    def run_server(self):
        # pylint: disable=attribute-defined-outside-init
        self.server_thread = threading.Thread(target=self._run_server)
        self.server_thread.start()

    def __get_image(self, docker_client):
        path = self.__get_base_path()

        sys.stdout.write(f'Building {path}')

        try:
            image, logs = docker_client.images.build(
                path=path,
                dockerfile='./clai/emulator/docker/centos/Dockerfile',
                rm=True
            )

            for line in logs:
                sys.stdout.write('.')
                sys.stdout.flush()

        finally:
            sys.stdout.write('\n')

        return image

    def _run_server(self):
        self.server_running = True
        self.on_server_running()

        docker_client = docker.from_env()

        image = self.__get_image(docker_client)

        docker_container = docker_client.containers.run(
            image=image.id,
            detach=True)

        self.my_clai = Container(docker_container)

        wait_for_callable('Waiting for container to be ready', self.my_clai.ready)

        print(f"container run {self.my_clai.status}")

        self.request_skills()

        # self.server_process.wait()
        # stdout, stderr = self.server_process.communicate()
        # return_code = self.server_process.returncode
        # self.server_running = False
        # self.on_server_stopped()
        #
        # print(f"code {return_code}")
        # print(f"out {stdout}")
        # print(f"err {stderr}")
