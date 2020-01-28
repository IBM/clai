#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os
import subprocess
import threading
import time

from clai.server.agent_datasource import AgentDatasource
from clai.server.clai_client import send_command, send_command_post_execute
from clai.server.command_message import Action, ProcessesValues


# pylint: disable=too-many-instance-attributes
class EmulatorPresenter:
    def __init__(self, on_skills_ready, on_server_running, on_server_stopped):
        self.command_id = 0
        self.server_running = False
        self.server_process = None
        self.current_active_skill = ''
        self.agent_datasource = AgentDatasource()

        self.on_skills_ready = on_skills_ready
        self.on_server_running = on_server_running
        self.on_server_stopped = on_server_stopped

    def stop_server(self):
        if self.server_process:
            self.server_process.kill()

    def select_skill(self, skill_name: str, installed: bool):
        if skill_name == self.current_active_skill:
            return

        if installed:
            self._send_select(skill_name)
            self._send_unselect(self.current_active_skill)

        else:
            if self.install_skill(skill_name):
                self._send_select(skill_name)
                self._send_unselect(self.current_active_skill)

        self.request_skills()

    def request_skills(self):
        response = self._send_to_emulator("clai skills")

        skills_as_string = response.description
        skills_as_array = skills_as_string.splitlines()
        print(f"skills: {skills_as_array[1:-1]}")
        self.on_skills_ready(skills_as_array)

    def install_skill(self, skill_name: str) -> bool:
        agent_descriptor = self.agent_datasource.get_agent_descriptor(skill_name)

        exec_message = subprocess.Popen(
            f"sh {os.getcwd()}/../clai/emulator/emufileExist.sh {agent_descriptor.pkg_name}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdout, stderr = exec_message.communicate()
        result_code = exec_message.returncode
        print(f"code {result_code}")
        print(f"err {stderr}")
        print(f"out {stdout}")
        if result_code == 0:
            self.agent_datasource.mark_plugins_as_installed(skill_name, "user")
        return result_code == 0

    def send_message(self, message):
        response = self._send_to_emulator(message, increase_id=False)
        command_to_execute = response.suggested_command
        if not response.suggested_command:
            command_to_execute = response.origin_command
        exec_message = subprocess.Popen(command_to_execute,
                                        shell=True,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
        _, stderr = exec_message.communicate()
        result_code = exec_message.returncode

        print(result_code, stderr)

        response_post = self._send_to_emulator_post_command(result_code, stderr)
        return response, response_post

    def _send_select(self, skill_name: str):
        self._send_to_emulator(f'clai select {skill_name}')

    def _send_unselect(self, skill_name: str):
        self._send_to_emulator(f'clai unselect {skill_name}')

    def _send_to_emulator(self, command: str, increase_id: bool = True) -> Action:
        response = send_command(
            command_id=self.command_id,
            user_name="user",
            command_to_check=command,
            host="localhost",
            port=8020)
        if increase_id:
            self.command_id = self.command_id + 1
        return response

    def _send_to_emulator_post_command(self, result_code, stderr):
        response_post = send_command_post_execute(
            command_id=self.command_id,
            user_name="user",
            result_code=result_code,
            stderr=stderr,
            processes=ProcessesValues(last_processes=[]),
            host="localhost",
            port=8020
        )
        self.command_id = self.command_id + 1
        return response_post

    def run_server(self):
        # pylint: disable=attribute-defined-outside-init
        self.server_thread = threading.Thread(target=self._run_server)
        self.server_thread.start()

    def _run_server(self):
        self.server_running = True
        self.on_server_running()

        self.server_process = subprocess.Popen(["python3", f"{os.getcwd()}/clai-run", "new", "--port", "8020"],
                                               shell=False,
                                               stdout=subprocess.PIPE,
                                               stderr=subprocess.PIPE)

        print(f"process id {self.server_process.pid}")

        time.sleep(1)
        self.request_skills()

        self.server_process.wait()
        stdout, stderr = self.server_process.communicate()
        return_code = self.server_process.returncode
        self.server_running = False
        self.on_server_stopped()

        print(f"code {return_code}")
        print(f"out {stdout}")
        print(f"err {stderr}")
