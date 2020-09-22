#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import re

from enum import Enum
from typing import List, Dict
from urllib.parse import urljoin

from . import Provider

# Define permissible search scopings for KnowledgeCenter
class KCscope(Enum):
    ZOS_ALL = "SSLTBW"
    ZOS_210 = "SSLTBW_2.1.0"
    ZOS_220 = "SSLTBW_2.2.0"
    ZOS_230 = "SSLTBW_2.3.0"
    ZOS_240 = "SSLTBW_2.4.0"


# Define permissible types for KnowledgeCenter searches
class KCtype(Enum):
    DOCUMENTATION = ""
    DEVELOPERWORKS = "dw"
    REDBOOKS = "redbooks"
    TECHNOTES = "technotes"


class KnowledgeCenter(Provider):
    def __init__(self, name: str, description: str, section: dict):
        super().__init__(name, description, section)

        # Make sure that the variant searches specified (if any) are valid
        for variant in self.get_variants():
            if variant.name not in KCtype.__members__.keys():
                raise AttributeError(
                    f"Invalid {self.name} search variant: '{variant.name}'"
                )

        self.__log_debug__("z/OS KnowledgeCenter provider initialized")

    def get_variants(self) -> List[KCtype]:
        """Override the default get_variants() method so that it instead returns
        a list of KCtype objects"""
        types = []
        for type_str in super().get_variants():
            types.append(KCtype[type_str])
        return types

    def call(self, query: str, limit: int = 1, **kwargs):
        """Call the KnowledgeCenter search provider.  If no search variants
        were specified in the configuration file, we will default to searching
        the KnowledgeCenter documentation (ie: IBM publications) library"""
        kwargs = self.__set_default_values__(
            kwargs,
            search_type=KCtype.DOCUMENTATION,
            products=KCscope.ZOS_240,
            tags="bpx",
        )
        self.__log_debug__(
            f"call(query={query}, limit={str(limit)}, **kwargs={str(kwargs)})"
        )

        search_type: KCtype = kwargs["search_type"]
        target: str = urljoin(self.base_uri, search_type.value)
        payload = {"query": query, "offset": 0, "limit": limit, "tags": kwargs["tags"]}

        products: KCscope = kwargs["products"]
        if search_type in (KCtype.DOCUMENTATION, KCtype.TECHNOTES):
            payload["products"] = products.value

        request = self.__send_get_request__(target, params=payload)
        if request.status_code == 200:
            # self.__log_debug__(f"Response JSON: {str(request.json())}")

            # All 200 responses from the KnowledgeCenter begin with the header:
            #   {
            #       "offset": int,
            #       "next": int,
            #       "prev": int,
            #       "count": int,
            #       "total": int,
            #       ...
            if request.json()["count"] > 0:

                # The next field is either:
                #       "topics": [{...}, ...]
                # or is:
                #       "results": [{...}, ...]
                if search_type == KCtype.DOCUMENTATION:
                    return request.json()["topics"]

                return request.json()["results"]

        return None

    def extract_search_result(self, data: List[Dict]) -> str:
        self.__log_debug__(f"extract_search_result() returns {data[0]['summary']}")
        return data[0]["summary"]

    def get_printable_output(self, data: List[Dict]) -> str:

        # If the data contains a "products" tag, then this is the result of
        # a KCtype.DOCUMENTATION query, and will be of the form:
        #       "topics": [
        #           {
        #               "href": str,
        #               "products": [
        #                   {
        #                       "label": str,
        #                       "href": str
        #                   },
        #                   ...
        #               ],
        #               "tags": List[str],
        #               "date": int,
        #               "label": str,
        #               "summary": str
        #           },
        #           ...
        #       ]
        if "products" in data[0].keys():
            topic: Dict = data[0]
            product: Dict = topic["products"][0]
            lines = [
                f"Product: {product['label']}",
                f"Topic: {__clean__(topic['label'][:384] + ' ...')}",
                f"Answer: {__clean__(topic['summary'][:256] + ' ...')}",
                f"Tags: {str(topic['tags'])}",
                f"Link: https://www.ibm.com/support/knowledgecenter/{topic['href']}\n",
            ]

        # Otherwise, this data is the result of a KCtype.DEVELOPERWORKS, REDBOOKS,
        # or TECHNOTES query, and will be of the form:
        #   {
        #       "results": [
        #           {
        #               "date": int,
        #               "link": str,
        #               "title": str,
        #               "summary": str,
        #               "tags": List[str],
        #               "foundIn": [
        #                   {
        #                       "productID": str,
        #                       "productName": str,
        #                       "href": str
        #                   },
        #                   ...
        #               ]
        #           },
        #           ...
        #       ]
        else:
            result: Dict = data[0]
            lines = [
                f"Title: {__clean__(result['title'][:384] + ' ...')}",
                f"Answer: {__clean__(result['summary'][:256] + ' ...')}",
                f"Link: {result['link']}\n",
            ]

        self.__log_debug__(f"get_printable_output() returns {str(lines)}")
        return "\n".join(lines)

def __clean__(html: str) -> str:
    return re.sub(re.compile("<.*?>"), "", html)
