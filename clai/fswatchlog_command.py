#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from typing import List

from clai.server.clai_client import send_files
from clai.server.command_message import (
    FilesChangesValues,
    FileChange,
    FileStatus,
    FileType,
)


def split_file_commands(list_to_chunk: List, size_chunk: int):
    return [
        list_to_chunk[i : i + size_chunk]
        for i in range(0, len(list_to_chunk), size_chunk)
    ]


def is_type(type_as_string: str) -> bool:
    return type_as_string in ("IsFile", "IsDir")


def map_type(type_as_string) -> FileType:
    if type_as_string == "IsFile":
        return FileType.File

    if type_as_string == "IsDir":
        return FileType.Dir

    return FileType.Unknow


def is_status(status: str) -> bool:
    return status in ("Created", "Removed", "Renamed", "Updated", "OwnerModified")


def map_status(status_as_string: str) -> FileStatus:
    if status_as_string == "Created":
        return FileStatus.New

    if status_as_string == "Removed":
        return FileStatus.Deleted

    if status_as_string in ("Renamed", "Updated", "OwnerModified"):
        return FileStatus.Modified

    return FileStatus.Unknow


def map_files(files_args) -> List[FileChange]:
    if not files_args:
        return []

    cont = 0
    files = []
    value_to_add = files_args[cont]
    current_file = None
    while value_to_add != "NoOp":
        if value_to_add.startswith("/"):
            if current_file is not None:
                files.append(current_file)
            current_file = FileChange(filename=value_to_add)
        elif is_status(value_to_add):
            current_file.status.append(map_status(value_to_add))
        elif is_type(value_to_add):
            current_file.file_type = map_type(value_to_add)
        cont += 1
        value_to_add = files_args[cont]
    return files


def process_files(command_id, user_name, files_changes):
    files_to_send = map_files(files_changes)

    send_files(
        command_id=command_id,
        user_name=user_name,
        files_values=FilesChangesValues(
            user_files=files_to_send, working_directory_files=[]
        ),
    )
