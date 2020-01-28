#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os


def check_if_process_running() -> bool:
    return os.system('ps -Ao args | grep "[c]lai-run" > /dev/null 2>&1') == 0
