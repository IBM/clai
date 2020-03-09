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
from clai.emulator.emulator_docker_bridge import EmulatorDockerBridge, get_base_path

# pylint: disable=too-many-instance-attributes
from clai.server.command_message import Action

from clai.server.command_runner.clai_last_info_command_runner import InfoDebug
from clai.tools.docker_utils import execute_cmd


class EmulatorPresenter:
    def __init__(self, emulator_docker_bridge: EmulatorDockerBridge, on_skills_ready, on_server_running,
                 on_server_stopped):
        self.server_running = False
        self.server_process = None
        self.current_active_skill = ''
        self.emulator_docker_bridge = emulator_docker_bridge

        self.on_skills_ready = on_skills_ready
        self.on_server_running = on_server_running
        self.on_server_stopped = on_server_stopped
        self.log_value = ""
        self.log_read = None

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
        self.emulator_docker_bridge.request_skills()

    def send_message(self, message):
        self.emulator_docker_bridge.send_message(message)

    def attach_log(self, chunked_read):
        self.log_read = chunked_read

    def _send_select(self, skill_name: str):
        self.emulator_docker_bridge.select_skill(skill_name)

    def _send_unselect(self, skill_name: str):
        self.emulator_docker_bridge.unselect_skill(skill_name)

    def _send_to_emulator(self, command: str) -> str:
        response = execute_cmd(self.my_clai, command)
        return response

    def run_server(self):
        self.emulator_docker_bridge.start()
        self.server_running = True
        self.on_server_running()
        self.request_skills()

    def refresh_files(self):
        self.copy_files()
        self._send_to_emulator("clai reload")

    def copy_files(self):
        old_path = os.getcwd()
        print(f'Building {old_path}')
        srcpath = os.path.join(get_base_path(),
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

    def retrieve_messages(self, add_row):
        reply = self.emulator_docker_bridge.retrieve_message()
        if reply:
            if reply.docker_reply == 'skills':
                skills_as_array = reply.message.splitlines()
                self.on_skills_ready(skills_as_array[2:-1])
            elif reply.docker_reply == 'reply_message':
                info_as_string = reply.info[reply.info.index('{'):]
                info_as_string = info_as_string[:info_as_string.index('\n')]
                print(f"----> {info_as_string}")
                info = InfoDebug(**json.loads(info_as_string))
                add_row(reply.message, info)
            elif reply.docker_reply == 'log':
                self.log_value = self.extract_chunk_log(self.log_value, reply.message)
                if self.log_read:
                    self.log_read(self.log_value)
            else:
                print(f"-----> {reply.docker_reply} : {reply.message}")

    def extract_chunk_log(self, log_value, message):
        if not message:
            return ''

        log_as_list = log_value.split('\n')
        message_as_list = message.split('\n')

        new_log = []
        if log_as_list.__contains__(message_as_list[0]):
            index = log_as_list.index(message_as_list[0])
            new_log = message_as_list[(len(log_as_list) - index - 1):]
        else:
            new_log = message_as_list

        return '\n'.join(new_log)
