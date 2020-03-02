#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#
from typing import Optional

from pydantic import BaseModel

from clai.datasource.server_status_datasource import ServerStatusDatasource
from clai.server.command_message import State, Action, ProcessesValues, FilesChangesValues, NetworkValues
from clai.server.command_runner.command_runner import CommandRunner, PostCommandRunner


# pylint: disable=too-few-public-methods
class ClaiLastInfoCommandRunner(CommandRunner, PostCommandRunner):
    LAST_DIRECTIVE_DIRECTIVE = 'clai last-info'

    def __init__(self, server_status_datasource: ServerStatusDatasource):
        self.server_status_datasource = server_status_datasource

    def execute(self, state: State) -> Action:
        return Action(suggested_command=":",
                      execute=True,
                      origin_command=state.command
                      )

    def execute_post(self, state: State) -> Action:
        offset_last = state.command.replace(f'{self.LAST_DIRECTIVE_DIRECTIVE}', '').strip()
        if not offset_last:
            return Action()

        if not offset_last.isdigit():
            return Action()

        offset_last_as_int = int(offset_last)
        last_message = self.server_status_datasource.get_last_message(state.user_name, offset=offset_last_as_int)

        if not last_message:
            return Action()

        info_to_show = InfoDebug(
            command_id=last_message.command_id,
            user_name=last_message.user_name,
            command=last_message.command,
            root=last_message.root,
            processes=last_message.processes,
            file_changes=last_message.file_changes,
            network=last_message.network,
            result_code=last_message.result_code,
            stderr=last_message.stderr,
            already_processed=last_message.already_processed,
            action_suggested=last_message.action_suggested
        )

        return Action(
            description=str(info_to_show.json())
        )


class InfoDebug(BaseModel):
    command_id: str
    user_name: str
    file_changes: Optional[FilesChangesValues] = None
    command: str = None
    root: bool = False
    processes: Optional[ProcessesValues] = ProcessesValues()
    network: Optional[NetworkValues] = None
    result_code: Optional[str] = None
    stderr: Optional[str] = None
    already_processed: bool = False
    action_suggested: Optional[Action] = None
    action_post_suggested: Optional[Action] = None
