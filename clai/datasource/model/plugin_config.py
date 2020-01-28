#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from typing import Dict, List, Union

from pydantic import BaseModel


# pylint: disable=too-few-public-methods,dangerous-default-value,too-many-arguments
class PluginConfig:
    def __init__(self,
                 selected: List[str] = [],
                 default: List[str] = [],
                 installed: List[str] = [],
                 report_enable: bool = False):
        self.selected = selected
        self.default = default
        self.installed = installed
        self.report_enable = report_enable


class PluginConfigJson(BaseModel):
    selected: Dict[str, list] = {}
    default: Union[List[str], str] = ["demo_agent"]
    installed: List[str] = []
    report_enable: bool = False
