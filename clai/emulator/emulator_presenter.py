#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#
import json
import os
import sys
import tarfile
import threading
from typing import Optional

import docker
from pytest_docker_tools.utils import wait_for_callable
from pytest_docker_tools.wrappers import Container

from clai.server.agent_datasource import AgentDatasource

# pylint: disable=too-many-instance-attributes
from clai.server.command_runner.clai_last_info_command_runner import InfoDebug
from clai.tools.docker_utils import execute_cmd, stream_cmd


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
        if 'bin' in root_path:
            return '../'

        return '.'

    def stop_server(self):
        print(f'is server running {self.server_running}')
        if self.server_running:
            self.my_clai.kill()
            self.server_running = False
        self.on_server_stopped()

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

        stdout = self._send_to_emulator(message)
        info_as_string = self._send_to_emulator("clai last-info 1")
        info_as_string = info_as_string[info_as_string.index('{'):]
        info_as_string = info_as_string[:info_as_string.index('\n')]
        print(f"----> {info_as_string}")
        info = InfoDebug(**json.loads(info_as_string))

        return stdout, info

    def attach_log(self, chunked_read):
        stdout = self._send_to_emulator('tail -f /var/tmp/app.log')
        chunked_read(stdout)

    def _send_select(self, skill_name: str):
        self._send_to_emulator(f'clai activate {skill_name}')

    def _send_unselect(self, skill_name: str):
        self._send_to_emulator(f'clai deactivate {skill_name}')

    def _send_to_emulator(self, command: str) -> str:
        response = execute_cmd(self.my_clai, command)
        return response

    def _stream_message(self, command: str, chunked_readed):
        stream_cmd(self.my_clai, command, chunked_readed)

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

            for _ in logs:
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

    def refresh_files(self):
        self.copy_files()
        self._send_to_emulator("clai reload")

    def copy_files(self):
        old_path = os.getcwd()
        print(f'Building {old_path}')
        srcpath = os.path.join(self.__get_base_path(),
                               'clai', 'server', 'plugins')
        os.chdir(srcpath)

        tar = tarfile.open('temp.tar', mode='w')
        try:
            tar.add('.', recursive=True)
        finally:
            tar.close()

        data = open('temp.tar', 'rb').read()

        destdir = os.path.join(
            os.path.expanduser('/opt/local/share'),
            'clai', 'bin', 'clai', 'server', 'plugins'
        )

        # pylint: disable=protected-access
        self.my_clai._container.put_archive(destdir, data)

        os.chdir(old_path)

        print("Done the refresh")
