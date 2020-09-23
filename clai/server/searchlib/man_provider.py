#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from typing import List, Dict

from clai.server.searchlib.providers import Provider


class Manpages(Provider):
    def __init__(self, name: str, description: str, section: dict):
        super().__init__(name, description, section)
        self.__log_debug__("Manpages provider initialized")

    def call(self, query: str, limit: int = 1, **kwargs):
        self.__log_debug__(
            f"call(query={query}, limit={str(limit)}), **kwargs={str(kwargs)})"
        )

        payload = {"text": query, "result_count": limit}

        request = self.__send_post_request__(self.base_uri, params=payload)
        if request.status_code == 200:
            return request.json()

        return None

    def extract_search_result(self, data: List[Dict]) -> str:
        pass

    def get_printable_output(self, data: List[Dict]) -> str:
        pass
