#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

''' tar command handler '''

''' imports '''
import requests

''' globals '''
wa_endpoint = 'http://nlc2cmd-chipper-impala.us-east.mybluemix.net/tarbot'

def wa_skill_processor_tarbot(msg):

    # Confidence remains at 0 and data is None unless an intent has been detected
    confidence = 0.0
    data = None

    if msg.startswith('tar'):
        return None, 0.0

    try:
        response = requests.put(wa_endpoint, json={'text': msg}).json()

        if response['result'] == 'success':
            response = response['response']['output']
        else:
            return [ { "text" : response['result'] }, confidence ]

    except Exception as ex:
        return [ { "text" : "Method failed with status " + str(ex) }, confidence ]

    # Identify the intent in the user message
    try:

        intent = response["intents"][0]["intent"]
        confidence = response["intents"][0]["confidence"]

    except IndexError or KeyError:
        intent = "xkcd"

    # Identify entities in the user message
    entities = {}
    for item in response["entities"]:

        if item['entity'] in entities:
            entities[item['entity']].append(item['value'])
        else:
            entities[item['entity']] = [item['value']]

    # Identify file and directory name if present
    filename = "<archive-file>"
    dirname = "<directory>"

    # Fixed supported extensions
    extensions = {"images": ['.png, .bmp, .jpg'], "documents": [".doc", ".docx", ".txt", ".pdf", ".md"]}

    # Configure flags based on entities
    flags = ""
    if 'verbose' in entities:
        flags += "v"

    if 'tar-type' in entities:

        if "gz" in entities['tar-type']:
            flags += "z"
        elif "bz2" in entities['tar-type']:
            flags += "j"

    # Configure command based on intent

    intents = {'check-size': {"text": "Try >> tar -czf - {} | wc -c".format(filename)},
               'check-validity': {"text": "Try >> tar tvfW {}".format(filename)},
               'tar-usage': {"text": "Tar Usage and Options: \nc – create a archive file. "
                                     "\nx – extract a archive file. \nv – show the progress of archive file. "
                                     "\nf – filename of archive file. \nt – viewing content of archive file.  "
                                     "\nj – filter archive through bzip2.  \nz – filter archive through gzip. "
                                     "\nr – append or update files or directories to existing archive file.  "
                                     "\nW – Verify a archive file.  wildcards – Specify patterns in unix tar "
                                     "command."}}

    if intent in intents:
        data = intents[intent]

    elif intent == "tar-directory-to-file":
        flags = "c{}f".format(flags) 
        data = {"text": "Try >> tar -{} {} {}".format(flags, filename, dirname)}

    elif intent == "untar-file-to-directory":
        flags = "x{}f".format(flags) 
        if 'directory-name' in entities:
            data = {"text": "Try >> tar -{} {} -C {}".format(flags, filename, dirname)}
        else:
            data = {"text": "Try >> tar -{} {}".format(flags, filename)}

    elif intent == "untar-group-of-files":
        flags = "x{}f".format(flags) 
        ext = []

        if 'file-extension' in entities:
            ext += entities['file-extension']
        elif 'file-type' in entities:
            ext += extensions[entities['file-type'][0]]

        if not ext:
            ext = [".ext"]

        if 'directory-name' in entities:
            data = {"text": "Try >> tar -{} {} --wildcards {} -C {}".format(flags, filename,
                                                                           ' '.join(["*" + e for e in ext]),
                                                                           dirname)}
        else:
            data = {
                "text": "Try >> tar -{} {} --wildcards {}".format(flags, filename, ' '.join(["*" + e for e in ext]))}

    elif intent == "untar-single-file":
        flags = "x{}f".format(flags) 

        if 'directory-name' in entities:
            data = {"text": "Try >> tar -{} {} -C {}".format(flags, filename, dirname)}
        else:
            data = {"text": "Try >> tar -{} {}".format(flags, filename)}

    elif intent == "add-to-file":
        flags = "{}rf".format(flags) 

        if 'tar-type' in entities:
            if "gz" in entities['tar-type'] or "bz2" in entities['tar-type']:
                data = {
                    "text": "The tar command don’t have a option to add files or directories to an existing "
                            "compressed tar.gz and tar.bz2 archive file."}
            else:
                data = {"text": "Unrecognized option."}

        else:
            data = {"text": "Try >> tar -{} {} <file>".format(flags, filename)}

    elif intent == "list-contents":

        flags = "{}tf".format(flags) 
        ext = []

        if 'file-extension' in entities:
            ext += entities['file-extension']
        elif 'file-type' in entities:
            ext += extensions[entities['file-type'][0]]

        if not ext:
            data = {"text": "Try >> tar -{} {}".format(flags, filename)}
        else:
            data = {"text": "Try >> tar -{} {} '{}'".format(flags, filename, ' '.join(["*" + e for e in ext]))}

    else: pass

    return data, confidence




