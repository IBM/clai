#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import multiprocessing as mp

import amplitude

from clai.datasource.model.stat_event import StatEvent
from clai.server.agent_datasource import AgentDatasource
from clai.server.logger import current_logger as logger
from clai.tools.anonymizer import Anonymizer


def __send_event__(event: StatEvent):
    try:
        amplitude_logger = amplitude.AmplitudeLogger(api_key="cc826565c91ab899168235a2845db189")
        event_args = {"device_id": event.user, "event_type": event.event_type,
                      "event_properties": event.data
                      }
        event = amplitude_logger.create_event(**event_args)
        amplitude_logger.log_event(event)
    # pylint: disable=broad-except
    except Exception as ex:
        logger.info(f"error tracking event {ex}")


class StatsTracker:
    def __init__(self, sync=False, anonymizer: Anonymizer = Anonymizer()):
        if not sync:
            self.manager = mp.Manager()
            self.queue = self.manager.Queue()
            self.pool = mp.Pool(1)
            self.consumer_stats = None

        self.anonymizer = anonymizer
        self.report_enable = False

    @staticmethod
    def consumer(queue):
        while True:
            event = queue.get()

            if event is None:
                break

            logger.info(f"send_event: {event}")
            __send_event__(event)
            queue.task_done()
        logger.info("----STOP CONSUMING-----")

    def start(self, agent_datasource: AgentDatasource):
        logger.info(f"-Start tracker-")
        self.report_enable = agent_datasource.get_report_enable()
        if self.report_enable:
            self.consumer_stats = self.pool.map_async(self.consumer, (self.queue,))

    def wait(self):
        if self.report_enable:
            self.__store__(None)
            self.consumer_stats.wait(timeout=3)


    def log_activate_skills(self, user: str, skill_name: str):
        event = StatEvent(
            event_type="activate",
            user=self.anonymizer.anonymize(user),
            data={"skill": f"{skill_name}"}
        )
        self.__store__(event)

    def log_deactivate_skills(self, user: str, skill_name: str):
        event = StatEvent(
            event_type="deactivate",
            user=self.anonymizer.anonymize(user),
            data={"skill": f"{skill_name}"}
        )
        self.__store__(event)

    def log_install(self, user: str):
        if not self.report_enable:
            return

        event = StatEvent(
            event_type="install",
            user=self.anonymizer.anonymize(user),
            data={}
        )

        __send_event__(event)

    def log_uninstall(self, user: str):
        if not self.report_enable:
            return

        event = StatEvent(
            event_type="uninstall",
            user=self.anonymizer.anonymize(user),
            data={}
        )

        __send_event__(event)

    def __store__(self, event: StatEvent):
        if not self.report_enable:
            return

        try:
            logger.info(f"record stats -> {event}")
            self.queue.put(event)
        # pylint: disable=broad-except
        except Exception as err:
            logger.info(f"error sending: {err}")


# pylint: disable= invalid-name
stats_tracker = StatsTracker()
