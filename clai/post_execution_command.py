#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import importlib
from typing import List
from clai import PLATFORM
from clai.server.clai_client import send_command_post_execute
from clai.server.command_message import Process, ProcessesValues

try:
    PSUTIL = importlib.import_module("psutil")
except ImportError:
    if PLATFORM != "zos":
        print("Error: psutil not installed")


EXCLUDE_OWN_PROCESS = 1
SIZE_PROCESS = 11


def map_processes(processes) -> List[Process]:
    return list(map(lambda _: Process(name=_["name"]), processes))


def obtain_last_processes(user_name):
    process_changes = []

    if PLATFORM != "zos":
        for process in PSUTIL.process_iter(
                attrs=["pid", "name", "username", "create_time"]
        ):
            process_changes.append(process.info)
    else:
        # TODO: Figure out the equivalent on z/OS
        pass

    porcess_changes = list(
        filter(lambda _: _["username"] == user_name, process_changes)
    )
    porcess_changes.sort(key=lambda _: _["create_time"], reverse=True)
    return map_processes(process_changes[EXCLUDE_OWN_PROCESS:SIZE_PROCESS])


def post_process_command(command_id: str, user_name: str, cmd_result: str, stderr: str):
    process_changes = obtain_last_processes(user_name)
    post_command_action = send_command_post_execute(
        command_id=command_id,
        user_name=user_name,
        result_code=cmd_result,
        stderr=stderr,
        processes=ProcessesValues(last_processes=process_changes),
    )

    if stderr:
        print(stderr)

    if post_command_action and post_command_action.description:
        print(post_command_action.description)
