#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from typing import Optional, List, Union
from pathlib import Path
import os
import json
import numpy as np

from clai.server.orchestration.orchestrator import Orchestrator
from clai.server.command_message import State, Action


# pylint: disable=too-many-arguments,unused-argument
class MaxOrchestrator(Orchestrator):
    def __init__(self):
        super(MaxOrchestrator, self).__init__()

        self._config_path = os.path.join(
            Path(__file__).parent.absolute(), "config.json"
        )
        self.__read_config__()

    def __read_config__(self):

        with open(self._config_path, "r") as fileobj:
            config = json.load(fileobj)

        self.threshold = config["threshold"]

    def choose_action(
        self,
        command: State,
        agent_names: List[str],
        candidate_actions: Optional[List[Union[Action, List[Action]]]],
        force_response: bool,
        pre_post_state: str,
    ) -> Optional[Action]:
        """Choose an action for CLAI to respond with"""

        if not candidate_actions:
            return None

        confs = [self.__calculate_confidence__(action) for action in candidate_actions]
        idx_maxconf = np.argmax(confs)

        max_conf = confs[idx_maxconf]
        selected_candidate = candidate_actions[idx_maxconf]

        if force_response:
            return selected_candidate

        if max_conf >= self.threshold:
            return selected_candidate

        return None
