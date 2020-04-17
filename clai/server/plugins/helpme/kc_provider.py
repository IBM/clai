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
from typing import List, Dict

from clai.server.logger import current_logger as logger

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
    
    def __init__(self, name:str, section:dict):
        super().__init__(name, section)
    
    def call(self,
             query:str,
             limit:int = 1,
             products:KCscope = KCscope.ZOS_240,
             searchType:KCtype = KCtype.DOCUMENTATION
             ):

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

        r = requests.get(self.baseURI, params=payload, headers=headers)
        if r.status_code == 200:
            return r.json()['topics']

        return None
    
    def extractSearchResult(self, data:List[Dict]) -> str:
        return data[0]['summary']
    
    def getPrintableOutput(self, data:List[Dict]) -> str:
        result:Dict = data[0]
        product:Dict = result['products'][0]
        lines = [f"Product: {product['label']}",
                 f"Topic: {result['label'][:384] + ' ...'}",
                 f"Answer: {result['summary'][:256] + ' ...'}",
                 f"Link: https://www.ibm.com/support/knowledgecenter/{result['href']}\n"]
        
