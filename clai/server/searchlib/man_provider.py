#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import requests

from . import Provider
from typing import List, Dict

class Manpages(Provider):
    
    def __init__(self, name:str, description:str, section:dict):
        super().__init__(name, description, section)
    
    def call(self, query: str, limit: int = 1):
        self.__log_debug__(f"call(query={query}, limit={str(limit)})")
        
        payload = {
            'text': query,
            'result_count': limit
        }
        
        headers = {'Content-Type': "application/json"}
        self.__log_debug__(f"POST --> {str(self.baseURI)}\nheaders={str(headers)}\nparams={str(payload)}")
         
        r = requests.post(self.baseURI, params=payload, headers=headers)
        self.__log_debug__(f"Got HTTP response with RC={str(r.status_code)}")

        if r.status_code == 200:
            return r.json()

        return None
    
    def extractSearchResult(self, data:List[Dict]) -> str:
        pass
    
    def getPrintableOutput(self, data:List[Dict]) -> str:
        pass
