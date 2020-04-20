#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import abc
import os

from typing import List, Dict
from clai.server.logger import current_logger as logger

class Provider:
    
    # Define instance data members
    baseURI:str = ""
    excludes:list = []
    
    def __init__(self, name:str, description:str, section:dict):
        self.name = name
        self.description = description
        self.baseURI = section.get('api')
        
        # Get the platform exclusion list, in lowercase if possible
        if 'exclude' in section.keys():
            self.excludes = [excludeTarget.lower() for excludeTarget in section.get('exclude').split()]
        else:
            self.excludes = []
    
    def __str__(self) -> str:
        return self.description
    
    def __log_info__(self, message):
        logger.info(f"{self.name}: {message}")
        
    def __log_warning__(self, message):
        logger.warning(f"{self.name}: {message}")
    
    def __log_debug__(self, message):
        logger.debug(f"{self.name}: {message}")
    
    def getExcludes(self) -> list:
        return self.excludes
    
    def canRunOnThisOS(self) -> bool:
        """Returns True if this search provider can be used on the client OS
        """
        
        # If our exclusion list is empty, then this provider can work on any OS
        if len(self.excludes) == 0:
            return True
        
        os_name:str = os.uname().sysname.lower()
        return (os_name not in self.excludes)
    
    @abc.abstractclassmethod
    def extractSearchResult(self, data:List[Dict]) -> str:
        """Given the result of an API search, extract the search result from it
        """
        pass
    
    @abc.abstractclassmethod
    def getPrintableOutput(self, data:List[Dict]) -> str:
        """Return an informative string that can be displayed to the user
        """
        pass
    
    @abc.abstractclassmethod
    def call(self, query: str, limit: int = 1):
        pass
