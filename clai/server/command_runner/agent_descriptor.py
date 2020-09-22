#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

# pylint: disable=too-few-public-methods,too-many-arguments,dangerous-default-value,too-many-instance-attributes
class AgentDescriptor:
    def __init__(
        self,
        pkg_name,
        name,
        exclude=[],
        description="",
        installed=False,
        default=False,
        z_default=False,
    ):
        self.pkg_name = pkg_name
        self.name = name
        self.description = description
        self.default = default
        self.z_default = z_default
        self.installed = installed
        self.exclude = exclude
        self.ready = False
