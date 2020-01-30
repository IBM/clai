#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

# pylint: disable=too-many-instance-attributes,too-many-arguments,too-few-public-methods
from enum import Enum
from typing import Optional, List, Union
from copy import deepcopy
import os

from pydantic import BaseModel


class Process(BaseModel):
    name: str


class ProcessesValues(BaseModel):
    last_processes: List[Process]


class FileStatus(str, Enum):
    New = 'new'
    Modified = 'modified'
    Deleted = 'deleted'
    Unknow = 'unknow'


class FileType(str, Enum):
    File = "file"
    Dir = "dir"
    Unknow = "unknow"


class FileChange(BaseModel):
    filename: str
    status: List[FileStatus] = []
    file_type: FileType = None


class FilesChangesValues(BaseModel):
    user_files: List[FileChange]
    working_directory_files: List[FileChange]


class NetworkValues(BaseModel):
    has_network: bool


class StateDTO(BaseModel):
    command_id: str
    user_name: str
    command: str = None
    root: bool = False
    processes: Optional[ProcessesValues] = None
    file_changes: Optional[FilesChangesValues] = None
    network: Optional[NetworkValues] = None
    result_code: Optional[str] = None
    stderr: Optional[str] = None


class State:

    def __init__(self,
                 command_id: str,
                 user_name: str,
                 command: str = None,
                 root: bool = False,
                 processes: Optional[ProcessesValues] = None,
                 file_changes: Optional[FilesChangesValues] = None,
                 network: Optional[NetworkValues] = None,
                 result_code: Optional[str] = None,
                 stderr: Optional[str] = None,
                 previous_execution: Optional['State'] = None,
                 already_processed: bool = False,
                 action_suggested: 'Action' = None,
                 action_post_suggested: 'Action' = None
                 ):
        self.command_id = command_id
        self.command = command
        self.root = root
        self.processes = processes
        self.file_changes = file_changes
        self.network = network
        self.result_code = result_code
        self.stderr = stderr
        self.previous_execution = previous_execution
        self.user_name = user_name
        self.already_processed = already_processed
        self.action_suggested = action_suggested
        self.action_post_suggested = action_post_suggested
        self.values_executed = []
        self.suggested_executed = False

    def merge(self, state: 'State'):
        if state.command is not None:
            self.command = state.command
        if not self.root:
            self.root = state.root
        if self.processes is None:
            self.processes = state.processes
        if self.file_changes is None:
            self.file_changes = state.file_changes
        if self.network is None:
            self.network = state.network
        if self.result_code is None:
            self.result_code = state.result_code
        if self.stderr is None:
            self.stderr = state.stderr
        if not self.already_processed:
            self.already_processed = state.already_processed
        if not self.action_suggested:
            self.action_suggested = state.action_suggested
        if not self.action_post_suggested:
            self.action_post_suggested = state.action_post_suggested

    def is_post_process(self) -> bool:
        return self.result_code is not None

    def is_command(self):
        return self.command is not None

    def is_already_processed(self):
        return self.already_processed

    def mark_as_processed(self):
        self.already_processed = True


NOOP_COMMAND = ":"
BASEDIR = os.getenv('CLAI_BASEDIR',
                    os.path.join(os.path.expanduser('~'), '.clai'))


class Action(BaseModel):
    origin_command: Optional[str] = None
    suggested_command: Optional[str] = None
    execute: bool = False
    description: Optional[str] = None
    confidence: float = 0.0
    pending_actions: bool = False
    agent_owner: str = None

    def is_same_command(self):
        return not self.suggested_command or self.suggested_command == self.origin_command


class TerminalReplayMemory:
    def __init__(self, command: State, agent_names: List[str],
                 candidate_actions: Optional[List[Union[Action, List[Action]]]],
                 force_response: bool, suggested_command: Optional[Action]):
        self.command = deepcopy(command)
        self.agent_names = agent_names
        self.candidate_actions = deepcopy(candidate_actions)
        self.force_response = force_response
        self.suggested_command = deepcopy(suggested_command)


class TerminalReplayMemoryComplete:
    def __init__(self):
        self.pre_replay = None
        self.post_replay = None
