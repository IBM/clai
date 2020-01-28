#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import json
from clai.server.command_message import Action


def process_message(data: str) -> Action:
    return Action(**json.loads(data))
