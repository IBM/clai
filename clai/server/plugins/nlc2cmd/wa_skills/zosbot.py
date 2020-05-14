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

    # Identify entities in the user message
    entities = {}
    for item in response["entities"]:
        if item['entity'] in entities: entities[item['entity']].append(item['value'])
        else: entities[item['entity']] = [item['value']]

    if intent == "bpxmtext":
        data = {"text" : "bpxmtext <reasoncode>"}

    elif intent == "compile-c-code":
        data = {"text" : "xlc"}
    
    elif intent == "extattr":
        data = {"text" : "extattr [+alps] [-alps] [-Fformat] file ..."}
    
    elif intent == "obrowse":
        data = {"text" : "obrowse -r xx [file]"}
    
    elif intent == "oedit":
        data = {"text" : "oedit [–r xx] [file]"}
    
    elif intent == "oget":
        data = {"text" : "OGET 'pathname' mvs_data_set_name(member_name)"}
    
    elif intent == "oput":
        data = {"text" : "OPUT mvs_data_set_name(member_name) 'pathname'"}
    
    elif intent == "oeconsol":

        if 'iplinfo' in entities: data = {"text" : "oeconsol 'd iplinfo'"}
        elif 'command' in entities: data = {"text" : "oeconsol '<command>'"}
        else: data = {"text" : "oeconsol 'd parmlib'"}

    elif intent == "tso":
        data = {"text" : "tso [–o] [–t] TSO_command"}
    
    else: pass
    return data, confidence

