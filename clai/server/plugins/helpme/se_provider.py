#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import json
import requests

from clai.server.plugins.helpme.search_provider import Provider

class StackExchange(Provider):
    
    def __init__(self, section:dict):
        super().__init__(section)
    
    def call(self, query: str, limit: int = 1):

        payload = {
            'text': query,
            'limit': limit
        }

        headers = {'Content-Type': "application/json"}

        r = requests.post(self.baseURI, data=json.dumps(payload), headers=headers)

        if r.status_code == 200:
            return r.json()['hits']

        return None
    