#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import uuid


def obtain_command_id():
    commaind_id = uuid.uuid4()
    return str(commaind_id)
