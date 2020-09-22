#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os
import json
import configparser
from pathlib import Path

import requests


class Datastore:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(os.path.join(str(Path(__file__).parent.absolute()), "config.ini"))

        self.stack_exchange_api = config["API"].get("stack_exchange_api")
        self.manpage_api = config["API"].get("manpage_api")

    def __call_manpage_api__(self, query: str, limit: int = 1):

        payload = {"text": query, "result_count": limit}

        headers = {"Content-Type": "application/json"}

        r = requests.post(self.manpage_api, params=payload, headers=headers)

        if r.status_code == 200:
            return r.json()

        return None

    def __call_stack_exchange_api__(self, query: str, limit: int = 1):

        payload = {"text": query, "limit": limit}

        headers = {"Content-Type": "application/json"}

        r = requests.post(
            self.stack_exchange_api, data=json.dumps(payload), headers=headers
        )

        if r.status_code == 200:
            return r.json()["hits"]

        return None

    def search(self, query, service="stack_exchange", size=10):
        if service == "stack_exchange":
            res = self.__call_stack_exchange_api__(query, size)
        elif service == "manpages":
            res = self.__call_manpage_api__(query, size)
        else:
            raise AttributeError(
                "Please select stack_exchange or manpage as a choice for service"
            )

        return res
