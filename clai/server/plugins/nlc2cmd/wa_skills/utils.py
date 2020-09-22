#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

""" helper functions for wa skills package """

""" imports """
from typing import List

import requests
import json
import os

""" globals """
SUCCESS = True
FAILURE = False

_real_path = "/".join(os.path.realpath(__file__).split("/")[:-1])
_path_to_config_file = _real_path + "/config.json"

services = json.loads(open(_path_to_config_file).read())


""" call to remote host of WA service """


def call_wa_skill(msg: str, name: str) -> List:

    wa_endpoint = services[name]

    try:
        response = requests.put(wa_endpoint, json={"text": msg}).json()

        if response["result"] == "success":
            return response["response"]["output"], SUCCESS
        else:
            return response["result"], FAILURE

    except Exception as ex:
        return "Method failed with status " + str(ex), FAILURE


""" return name of file being run """


def get_own_name(file: str) -> str:
    return os.path.basename(file).replace(".py", "")
