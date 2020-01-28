#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import logging
import logging.handlers as handlers


class Logger:
    MAX_IN_MB = 100000000

    def __init__(self):

        log_formatter = logging.Formatter(
            '%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')
        self.logger = logging.getLogger('clai_logger')
        self.logger.setLevel(logging.INFO)
        self.log_handler = handlers.RotatingFileHandler(
            "/var/tmp/app.log",
            mode='a',
            maxBytes=Logger.MAX_IN_MB,
            backupCount=10,
            encoding=None,
            delay=0)
        self.log_handler.setLevel(logging.INFO)
        self.log_handler.setFormatter(log_formatter)
        self.logger.addHandler(self.log_handler)

    def info(self, text):
        self.logger.info(text)

    def warning(self, text):
        self.logger.warning(text)

    def debug(self, text):
        self.logger.debug(text)


# pylint: disable= invalid-name
current_logger = Logger()
