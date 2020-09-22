#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.tools.colorize_console import Colorize
import sys

try:
    import tldr
except Exception as _:
    pass

TLDR_AVAILABLE = "tldr" in sys.modules


def get_command_tldr(cmd):

    if not TLDR_AVAILABLE:
        return ""

    cmd_tldr = tldr.get_page(cmd)

    if cmd_tldr is None:
        return ""

    description = Colorize()

    for i, line in enumerate(cmd_tldr):
        line = line.rstrip().decode("utf-8")

        if i == 0:
            description.append("-" * 50 + "\n")

        if len(line) < 1:  # Empty line
            description.append("\n")
        elif line[0] == "#":
            line = line[1:]
            description.warning().append(line.strip() + "\n")
        elif line[0] == ">":  # Description line
            line = " " + line[1:]
            description.normal().append(line.strip() + "\n")
        elif line[0] == "-":  # Example line
            description.normal().append(line.strip() + "\n")
        elif line[0] == "`":  # Example command
            line = " " + line[1:-1]
            description.info().append(line.strip() + "\n")

    description.normal().append("summary provided by tldr package\n")
    description.normal().append("-" * 50 + "\n")

    return description.to_console()
