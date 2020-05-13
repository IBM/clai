#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

''' tar command handler '''

''' imports '''
from clai.server.plugins.nlc2cmd.wa_skills.utils import call_wa_skill, get_own_name

''' globals '''
__self = get_own_name(__file__) 

def wa_skill_processor_zosbot(msg):

    # Confidence remains at 0 and data is None unless an intent has been detected
    confidence = 0.0
    data = None

    response, success = call_wa_skill(msg, __self)
    if not success: return {"text" : response}, 0.0

    # Identify the intent in the user message
    try:

        intent = response["intents"][0]["intent"]
        confidence = response["intents"][0]["confidence"]

    except IndexError or KeyError:
        pass

    return data, confidence
