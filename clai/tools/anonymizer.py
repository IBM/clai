#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import json
import os
import uuid
from typing import Mapping, Optional

import clai


# pylint: disable=too-few-public-methods
class Anonymizer:
    def __init__(self, alternate_path: Optional[str] = None):
        self.__cache: Mapping[str, str] = None
        self.alternate_path = alternate_path

    def __get_config_path__(self):
        if self.alternate_path:
            return self.alternate_path

        base_dir = os.path.dirname(clai.tools.__file__)
        filename = os.path.join(base_dir, "../../anonymize.json")
        return filename

    def anonymize(self, key: str) -> str:
        if not self.__cache:
            self.__init_cache__()

        if key in self.__cache:
            return self.__cache[key]

        return self.__create_anonymize(key)

    def __init_cache__(self):
        path = self.__get_config_path__()

        if not os.path.exists(path):
            self.__cache = {}
            return

        with open(path) as verify_file:
            self.__cache = json.load(verify_file)

    def __create_anonymize(self, key: str) -> str:
        self.__cache[key] = str(uuid.uuid4())
        with open(self.__get_config_path__(), "w+") as json_file:
            json.dump(self.__cache, json_file)
        return self.__cache[key]
