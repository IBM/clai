#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import json

from typing import List, Dict
from clai.server.searchlib.providers import Provider


class StackExchange(Provider):
    def __init__(self, name: str, description: str, section: dict):
        super().__init__(name, description, section)
        self.__log_debug__("UNIX StackExchange provider initialized")

    def call(self, query: str, limit: int = 1, **kwargs):
        self.__log_debug__(
            f"call(query={query}, limit={str(limit)}), **kwargs={str(kwargs)})"
        )

        payload = {"text": query, "limit": limit}

        request = self.__send_post_request__(self.base_uri, data=json.dumps(payload))
        if request.status_code == 200:
            return request.json()["hits"]

        return None

    def extract_search_result(self, data: List[Dict]) -> str:
        return data[0]["Answer"]

    def get_printable_output(self, data: List[Dict]) -> str:
        lines = [
            f"Post: {data[0]['Content'][:384] + ' ...'}",
            f"Answer: {data[0]['Answer'][:256] + ' ...'}",
            f"Link: {data[0]['Url']}\n",
        ]

        return "\n".join(lines)
