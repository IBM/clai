#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai import PLATFORM

class Colorize:
    WARNING = "\033[91m"
    INFO = "\033[95m"
    COMPLETE = "\033[32m"
    NORMAL = "\033[0m"


    if PLATFORM in ('zos', 'os390'):
        EMOJI_ROBOT = '@'
        EMOJI_CHECK = '[x]'
        EMOJI_BOX = '[ ]'
    else:
        EMOJI_ROBOT = '\U0001F916'
        EMOJI_CHECK = '\u2611'
        EMOJI_BOX = '\u25FB'

    def __init__(self):
        self._text_complete = ""

    def append(self, text):
        self._text_complete += text
        return self

    def warning(self):
        self._text_complete += self.WARNING
        return self

    def info(self):
        self._text_complete += self.INFO
        return self

    def complete(self):
        self._text_complete += self.COMPLETE
        return self

    def normal(self):
        self._text_complete += self.NORMAL
        return self

    def emoji(self, emoji_code):
        self._text_complete += emoji_code
        return self

    def to_console(self):
        self._text_complete += self.NORMAL
        return self._text_complete
