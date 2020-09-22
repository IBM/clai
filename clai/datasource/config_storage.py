#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import json
import os
from typing import List, Optional

import clai.datasource
from clai.datasource.model.plugin_config import PluginConfig, PluginConfigJson


class ConfigStorage:
    def __init__(self, alternate_path: Optional[str] = None):
        self.alternate_path = alternate_path

    def get_config_path(self):
        if self.alternate_path:
            return self.alternate_path

        base_dir = os.path.dirname(clai.datasource.__file__)
        filename = os.path.join(base_dir, "../../configPlugins.json")
        return filename

    def read_all_user_config(self) -> PluginConfigJson:
        with open(self.get_config_path(), "r") as json_file:
            loaded = json.load(json_file)
            config_for_all_users = PluginConfigJson(**loaded)
            return config_for_all_users

    def read_config(self, user_name: Optional[str] = None) -> PluginConfig:
        selected = None
        config_for_all_users = self.read_all_user_config()
        if user_name in config_for_all_users.selected:
            selected = config_for_all_users.selected[user_name]

        if not selected:
            if isinstance(config_for_all_users.default, str):
                selected = [config_for_all_users.default]
            else:
                selected = config_for_all_users.default
        return PluginConfig(
            selected=selected,
            default=config_for_all_users.default,
            default_orchestrator=config_for_all_users.default_orchestrator,
            installed=config_for_all_users.installed,
            report_enable=config_for_all_users.report_enable,
            user_install=config_for_all_users.user_install,
        )

    def store_config(self, config: PluginConfig, user_name: str = None):
        current_config = self.read_all_user_config()
        with open(self.get_config_path(), "w") as json_file:
            if user_name:
                current_config.selected[user_name] = config.selected
            current_config.installed = config.installed
            current_config.report_enable = config.report_enable
            current_config.orchestrator = config.orchestrator
            current_config.user_install = config.user_install
            json_as_string = str(current_config.json())
            json_file.write(json_as_string)

    def load_installed(self) -> List[str]:
        current_config = self.read_all_user_config()
        return current_config.installed


# pylint: disable=invalid-name
config_storage = ConfigStorage()
