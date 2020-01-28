#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from typing import Mapping


# pylint: disable=too-few-public-methods
class StatEvent:
    def __init__(self, event_type: str, user: str, data: Mapping[str, str]):
        self.event_type = event_type
        self.data = data
        self.user = user
