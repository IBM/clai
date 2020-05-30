#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#


class Service:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):

        # Extract user input
        command = args[0]
        confidence = 0.0

        

        # return final command
        return [command, confidence]
