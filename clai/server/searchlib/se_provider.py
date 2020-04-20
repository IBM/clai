#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import json
import requests

from . import Provider
from typing import List, Dict

class StackExchange(Provider):
    
    def __init__(self, name:str, description:str, section:dict):
        super().__init__(name, description, section)
    
    def call(self, query: str, limit: int = 1):
        self.__log_debug__(f"call(query={query}, limit={str(limit)})")

        payload = {
            'text': query,
            'limit': limit
        }

        headers = {'Content-Type': "application/json"}
        
        self.__log_debug__(f"POST --> {str(self.baseURI)}\nheaders={str(headers)}\ndata={str(payload)}")
        
        r = requests.post(self.baseURI, data=json.dumps(payload), headers=headers)
        self.__log_debug__(f"Got HTTP response with RC={str(r.status_code)}")

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
    