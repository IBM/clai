#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import io

from clai.tools.file_util import read_history, get_history_file_name


def restore_history(original_command: str):
    lines = read_history()

    new_lines = __remove_clai_history__(lines, original_command + "\n")
    io.open(get_history_file_name(), "w").writelines(new_lines)


def __remove_clai_history__(lines, original_command):
    if not lines:
        return lines

    if original_command not in lines:
        return lines

    lines_from_last = lines[::-1]
    position = lines_from_last.index(original_command)
    position = len(lines) - position - 1
    if position > 0 and lines[position - 1] == original_command:
        position = position - 1
    new_lines = lines[: position + 1]
    return new_lines
