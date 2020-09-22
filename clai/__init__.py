#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from sys import platform as detect_platform
PLATFORM = None
PLATFORM = PLATFORM if PLATFORM is not None else detect_platform.lower()
