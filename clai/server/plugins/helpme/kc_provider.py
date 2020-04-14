#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from enum import Enum
import json
import requests

from clai.server.plugins.helpme.search_provider import Provider

# Define permissible search scopings for KnowledgeCenter
class KCscope(Enum):
    ZOS_ALL='SSLTBW'
    ZOS_210='SSLTBW_2.1.0'
    ZOS_220='SSLTBW_2.2.0'
    ZOS_230='SSLTBW_2.3.0'
    ZOS_240='SSLTBW_2.4.0'
    
# Define permissible types for KnowledgeCenter searches
class KCtype(Enum):
    DOCUMENTATION=''
    DEVELOPER='developerworks'
    TECHNOTES='technotes'
    REDBOOKS='redbooks'

class KnowledgeCenter(Provider):
    
    def __init__(self, section:dict):
        super().__init__(section)
    
    def call(self, query:str, limit:int = 1, products:KCscope=KCscope.ZOS_240):

        payload = {
            'query': query,
            'products': products,
            'intitle': True,
            'intext': True,
            'offset': 0,
            'limit': limit,
            'dedup': True,
            'fallback': True
        }

        headers = {'Content-Type': "application/json"}

        r = requests.post(self.baseURI, data=json.dumps(payload), headers=headers)

        if r.status_code == 200:
            return r.json()['hits']

        return None
