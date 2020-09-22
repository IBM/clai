#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

""" grep command handler """

""" imports """
import re

from clai.server.plugins.nlc2cmd.wa_skills.utils import call_wa_skill, get_own_name

""" globals """
__self = get_own_name(__file__)
__flags = {"line-number": "n", "match-case": "i", "count": "c", "verbose": "v"}


def wa_skill_processor_grepbot(msg):

    # Confidence remains at 0 unless an intent has been detected
    confidence = 0.0
    data = {}

    try:

        match_string = re.findall(r"\"(.+?)\"", msg)[0]
        msg = msg.replace('"{}"'.format(match_string), "")

    except:
        match_string = "<string>"

    response, success = call_wa_skill(msg, __self)
    if not success:
        return {"text": response}, 0.0

    if msg.startswith("grep for"):
        confidence = 1.0
    else:
        confidence = max([item["confidence"] for item in response["intents"]])

    filename = "<filename>"
    dirname = None

    for item in response["entities"]:
        if item["entity"] == "directory":
            dirname = "<directory>"

        if item["entity"] == "starts-with":
            match_string = "^" + match_string

        if item["entity"] == "ends-with":
            match_string = match_string + "$"

    flags = "-"
    if dirname:
        flags += "r"

    for intent in response["intents"]:
        if intent["confidence"] > 0.25 and intent["intent"] != "find":
            flags += __flags[intent["intent"]]

    if flags == "-":
        flags = ""

    command = 'grep {} "{}"'.format(flags, match_string)

    if dirname:
        command += " {}".format(dirname)
    else:
        command += " {}".format(filename)

    data = {"text": "Try >> " + command}
    return data, confidence
