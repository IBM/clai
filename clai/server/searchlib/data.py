#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import configparser
from collections import OrderedDict
from typing import List, Dict

from clai.server.logger import current_logger as logger
from clai.server.searchlib.se_provider import StackExchange
from clai.server.searchlib.kc_provider import KnowledgeCenter
from clai.server.searchlib.man_provider import Manpages


class Datastore:
    # Instance data members
    apis: OrderedDict = {}

    def __init__(self, inifile_path: str):
        config = configparser.ConfigParser()
        config.read(inifile_path)

        # Get a list of APIs defined in the config file
        for section in config.sections():
            if section == "stack_exchange":
                self.apis[section] = StackExchange(
                    section, "Unix StackExchange forums", config[section]
                )
            elif section == "ibm_kc":
                self.apis[section] = KnowledgeCenter(
                    section, "IBM KnowledgeCenter", config[section]
                )
            elif section == "manpages":
                self.apis[section] = Manpages(section, "manpages", config[section])
            else:
                raise AttributeError(f"Unsupported service type: '{section}'")

        logger.debug(f"Sections in {inifile_path}: {str(self.apis)}")

    def get_apis(self) -> OrderedDict:
        return self.apis

    def search(self, query, service="stack_exchange", size=10, **kwargs) -> List[Dict]:
        supported_services = self.apis.keys()

        if service in supported_services:
            service_provider = self.apis[service]
            res = service_provider.call(query, size, **kwargs)
        else:
            raise AttributeError(f"service must be one of: {str(supported_services)}")

        return res
