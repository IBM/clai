#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import abc

class Provider:
    
    # Define instance data members
    baseURI:str = ""
    excludes:list = []
    
    def __init__(self, section:dict):
        self.baseURI = section.get('api')
        
        # Get the platform exclusion list
        if 'exclude' in section.keys():
            self.excludes = section.get('exclude').split()
        else:
            self.excludes = []
    
    def getBaseURI(self) -> str:
        return self.baseURI
    
    def getExcludes(self) -> list:
        return self.excludes
    
    @abc.abstractmethod
    def call(self, query: str, limit: int = 1):
        pass
    
    def __str__(self) -> str:
        return self.baseURI
