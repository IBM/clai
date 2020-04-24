#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

#!/usr/bin/env python3
from clai.emulator.emulator_docker_bridge import EmulatorDockerBridge

if __name__ == '__main__':
    EMULATOR_DOCKER_BRIDGE = EmulatorDockerBridge()

    from clai.emulator.clai_emulator import ClaiEmulator
    EMULATOR = ClaiEmulator(EMULATOR_DOCKER_BRIDGE)
    EMULATOR.launch()
