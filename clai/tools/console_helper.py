#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.tools.colorize_console import Colorize


def print_complete(text):
    print(Colorize().complete().append(text).to_console())


def print_error(text):
    print(Colorize().warning().append(text).to_console())
