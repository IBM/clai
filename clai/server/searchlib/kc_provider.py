#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from enum import Enum
import requests

from . import Provider
from typing import List, Dict

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
    
    def __init__(self, name:str, description:str, section:dict):
        super().__init__(name, description, section)
        self.__log_debug__("Provider initialized")
    
    def call(self,
             query:str,
             limit:int = 1,
             products:KCscope = KCscope.ZOS_240,
             searchType:KCtype = KCtype.DOCUMENTATION
             ):
        self.__log_debug__(f"call(query={query}, limit={str(limit)}, products={str(products.value)}, searchType={str(searchType.value)})")
        
        payload = {
            'query': query,
            'products': products.value,
            'intitle': True,
            'intext': True,
            'offset': 0,
            'limit': limit,
            'dedup': True,
            'fallback': True
        }
        
        if searchType != KCtype.DOCUMENTATION:
            payload['type'] = searchType.value

        headers = {'Content-Type': "application/json", 'Accept': "*/*"}
        
        self.__log_debug__(f"GET --> {str(self.baseURI)}\nheaders={str(headers)}\nparams={str(payload)}")

        r = requests.get(self.baseURI, params=payload, headers=headers)
        self.__log_debug__(f"Got HTTP response with RC={str(r.status_code)}")
        
        if r.status_code == 200:
            return r.json()['topics']

        return None
    
    def extractSearchResult(self, data:List[Dict]) -> str:
        self.__log_debug__(f"extractSearchResult() returns {data[0]['summary']}")
        return data[0]['summary']
    
    def getPrintableOutput(self, data:List[Dict]) -> str:
        result:Dict = data[0]
        product:Dict = result['products'][0]
        lines = [f"Product: {product['label']}",
                 f"Topic: {result['label'][:384] + ' ...'}",
                 f"Answer: {result['summary'][:256] + ' ...'}",
                 f"Link: https://www.ibm.com/support/knowledgecenter/{result['href']}\n"]
        
        self.__log_debug__(f"getPrintableOutput() returns {str(lines)}")
        return "\n".join(lines)
