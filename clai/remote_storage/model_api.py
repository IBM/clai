#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from typing import Optional, List

from pydantic import BaseModel

from clai.server.command_message import (
    ProcessesValues,
    FilesChangesValues,
    NetworkValues,
    Action,
)


class StateApi(BaseModel):
    command_id: str = None
    user_name: str = None
    command: str = None
    root: bool = False
    processes: Optional[ProcessesValues] = None
    file_changes: Optional[FilesChangesValues] = None
    network: Optional[NetworkValues] = None
    result_code: str = None
    stderr: str = None


class TerminalReplayMemoryApi(BaseModel):
    command: StateApi
    agent_names: List[str]
    candidate_actions: List[Action]
    force_response: str
    suggested_command: List[Action]


class RecordToSendApi(BaseModel):
    bashbot_info: TerminalReplayMemoryApi
