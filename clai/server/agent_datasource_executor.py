#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from abc import ABC, abstractmethod
from concurrent import futures


# pylint: disable=too-few-public-methods
class AgentDatasourceExecutor(ABC):
    @abstractmethod
    def execute(self, load_agent, pkg_name):
        """execute all init agents"""


class ThreadAgentDatasourceExecutor(AgentDatasourceExecutor):
    NUM_WORKERS = 4

    def __init__(self):
        self.executor = futures.ThreadPoolExecutor(max_workers=self.NUM_WORKERS)

    def execute(self, load_agent, pkg_name):
        self.executor.submit(load_agent, pkg_name)


# pylint: disable= invalid-name
thread_agent_datasource_executor = ThreadAgentDatasourceExecutor()
