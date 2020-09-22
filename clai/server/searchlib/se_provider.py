#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import json

from . import Provider
from typing import List, Dict

class StackExchange(Provider):
    
    def __init__(self, name:str, description:str, section:dict):
        super().__init__(name, description, section)
        
        # This search provider doesn't support any variant searches
        for variant in self.getVariants():
            raise AttributeError(f"Invalid {self.name} search variant: '{variant}'")
        
        self.__log_debug__("Provider initialized")
    
    def call(self, query: str, limit: int = 1, **kwargs):
        self.__log_debug__(f"call(query={query}, limit={str(limit)}), **kwargs={str(kwargs)})")

        payload = {
            'text': query,
            'limit': limit
        }
        
        r = self.__send_post_request__(self.baseURI, data=json.dumps(payload))
        if r.status_code == 200:
            return r.json()['hits']

        return None
    
    def extractSearchResult(self, data:List[Dict]) -> str:
        return data[0]['Answer']
    
    def getPrintableOutput(self, data:List[Dict]) -> str:
        lines = [f"Post: {data[0]['Content'][:384] + ' ...'}",
                 f"Answer: {data[0]['Answer'][:256] + ' ...'}",
                 f"Link: {data[0]['Url']}\n"]
        
        return "\n".join(lines)
    