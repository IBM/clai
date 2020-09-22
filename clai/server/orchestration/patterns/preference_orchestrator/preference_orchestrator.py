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

from clai.server.orchestration.orchestrator import Orchestrator
from clai.server.command_message import State, Action


# pylint: disable=too-many-arguments,unused-argument,duplicate-code
class PreferenceOrchestrator(Orchestrator):
    def __init__(self):
        super(PreferenceOrchestrator, self).__init__()

        self._config_path = os.path.join(
            Path(__file__).parent.absolute(), "config.json"
        )
        self.__read_config()

    def __read_config(self):

        with open(self._config_path, "r") as fileobj:
            config = json.load(fileobj)

        self.threshold = config["threshold"]
        self.preferences = config["preferences"]

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

        cache_candidates = []
        for action in candidate_actions:
            confidence = self.__calculate_confidence__(action)

            # create list of candidate skills that came out above the threshold
            if confidence >= self.threshold:
                cache_candidates.append([action, confidence])

        # sort candidate list by confidence
        cache_candidates = sorted(cache_candidates, key=lambda x: x[1], reverse=True)

        for candidate in cache_candidates:
            # pass through all preferences and pick the candidate with
            # the highest confidence not violating any preference
            send_flag = True

            for preference in self.preferences:
                if candidate[0].agent_owner == preference[1]:
                    if preference[0] in [
                        item[0].agent_owner for item in cache_candidates
                    ]:
                        send_flag = False
                        break

            if send_flag:
                return candidate[0]

        if force_response:
            if cache_candidates:
                return cache_candidates[0][0]

            return None

        return None
