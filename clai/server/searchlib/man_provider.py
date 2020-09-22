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
    def __init__(self, name: str, description: str, section: dict):
        super().__init__(name, description, section)

        # This search provider doesn't support any variant searches
        for variant in self.getVariants():
            raise AttributeError(f"Invalid {self.name} search variant: '{variant}'")

        self.__log_debug__("Provider initialized")

    def call(self, query: str, limit: int = 1, **kwargs):
        self.__log_debug__(
            f"call(query={query}, limit={str(limit)}), **kwargs={str(kwargs)})"
        )

        payload = {"text": query, "result_count": limit}

        r = self.__send_post_request__(self.baseURI, params=payload)
        if r.status_code == 200:
            return r.json()

        return None

    def extractSearchResult(self, data: List[Dict]) -> str:
        pass

    def getPrintableOutput(self, data: List[Dict]) -> str:
        pass
