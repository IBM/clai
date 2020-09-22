#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import builtins


def spy_print(mocker):
    return mocker.spy(builtins, "print")


def mock_input_console(mocker, value):
    mocker.patch("builtins.input", return_value=value)
