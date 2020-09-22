#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

# itemgetter is faster than lambda functions for sorting
from operator import itemgetter

import clai.server.plugins.nlc2cmd.wa_skills as wa_skills
import threading

class Service:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):

        # call to WA evaluators
        def __compute(*args):
            result.append( eval('wa_skills.' + args[0])(args[1]) )

        # Extract user input
        msg = args[0]

        result = []
        threads = []

        for item in dir(wa_skills):
            if 'wa_skill_processor' in item:
                threads.append( threading.Thread(target=__compute, args=(item, msg)) )

        for t in threads: t.start()
        for t in threads: t.join()

        # return wa skill with the highest confidence
        return sorted(result, key=itemgetter(1), reverse=True)[0]
