#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from sys import platform as detect_platform

platform = None
platform = platform if platform is not None else detect_platform
