#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

''' imports '''
from typing import List

import requests 
import json
import os


''' globals '''
_real_path = '/'.join(os.path.realpath(__file__).split('/')[:-1])
_path_to_config_file = _real_path + '/config.json'

_config = json.loads( open(_path_to_config_file).read() )

_github_access_token = _config["github_personal_access_token"]
_path_to_log_file =_config["path_to_log_file"]


class Service:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):

        # Extract user input
        command = args[0]
        confidence = 1.0

        # print(open(_path_to_output_file).read())

        # return final command
        return [command, confidence]

# ss = Service()
# ss()
