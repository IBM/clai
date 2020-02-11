#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

''' cloud starter-sheet command handler '''

''' imports '''
import requests

''' globals '''
# wa_endpoint = 'http://nlc2cmd-chipper-impala.us-east.mybluemix.net/tarbot'
wa_endpoint = 'https://ibmcloud-helper.mybluemix.net/message'

def wa_skill_processor_cloudbot(msg):

    # Confidence remains at 0 unless an intent has been detected
    confidence = 0.0 

    if msg.startswith('ibmcloud'):
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

    # # Identify entities in the user message
    # entities = {}
    # for item in response["entities"]:
    #
    #     if item['entity'] in entities:
    #         entities[item['entity']].append(item['value'])
    #     else:
    #         entities[item['entity']] = [item['value']]
    #
    # # Identify file and directory name if present
    # filename = "<archive-file>"
    # dirname = "<directory>"
    #
    # # Fixed supported extensions
    # extensions = {"images": ['.png, .bmp, .jpg'], "documents": [".doc", ".docx", ".txt", ".pdf", ".md"]}
    #
    # # Configure flags based on entities
    # flags = ""
    # if 'verbose' in entities:
    #     flags += "v"
    #
    # if 'tar-type' in entities:
    #
    #     if "gz" in entities['tar-type']:
    #         flags += "z"
    #     elif "bz2" in entities['tar-type']:
    #         flags += "j"

    # Configure command based on intent

    # intents = {'check-size': {"text": "Try >> tar -czf - {} | wc -c".format(filename)},
    #            'check-validity': {"text": "Try >> tar tvfW {}".format(filename)},
    #            'tar-usage': {"text": "Tar Usage and Options: \nc – create a archive file. "
    #                                  "\nx – extract a archive file. \nv – show the progress of archive file. "
    #                                  "\nf – filename of archive file. \nt – viewing content of archive file.  "
    #                                  "\nj – filter archive through bzip2.  \nz – filter archive through gzip. "
    #                                  "\nr – append or update files or directories to existing archive file.  "
    #                                  "\nW – Verify a archive file.  wildcards – Specify patterns in unix tar "
    #                                  "command."}}

    intents = {'add_tag_resource': {"text": "Try >> ibmcloud resource tag-attach --tag-names TAG --resource-name NAME"},
               'assign_access_create_policy': {"text": "Try >> ibmcloud iam user-policy-create USER_NAME [OPTIONS]"},
               'create_access_group': {"text": "Try >> ibmcloud iam user-policy-create USER_NAME [OPTIONS]"},
               'create_api_key': {"text": "Try >> ibmcloud iam api-key-create NAME -d DESCRIPTION"},
               'create_org_cloudfoundry_services': {"text": "Try >> ibmcloud account org-create ORG_NAME"},
               'create_resource': {"text": "Try >> ibmcloud resource service-instance-create NAME SERVICE_NAME PLAN_NAME LOCATION"},
               'create_resource_group': {"text": "Try >> ibmcloud resource group create GROUP_NAME"},
               'create_space_services_org': {"text": "Try >> ibmcloud account space-create SPACE_NAME"},
               'help': {"text": "Try >> ibmcloud help COMMAND"},
               'install_plugin': {"text": "Try >> ibmcloud plugin install NAME"},
               'invite_user_to_account': {"text": "Try >> ibmcloud account user-invite USER_EMAIL"},
               'list_plugins': {"text": "Try >> ibmcloud plugin repo-plugins"},
               'list_services_resource_group': {"text": "Try >> ibmcloud resource service-instances -g GROUP_NAME"},
               'list_tags_account': {"text": "Try >> ibmcloud resource tags"},
               'list_users_in_account': {"text": "Try >> ibmcloud account users (works only for account owners)"},
               'login': {"text": "Try >> ibmcloud login"},
               'search_ibm_cloud_catalog': {"text": "Try >> ibmcloud catalog search QUERY"},
               'target_cloudfoundry_org': {"text": "Try >> ibmcloud target --cf"},
               'view_service_details': {"text": "Try >> ibmcloud catalog service NAME"},
               'view_usage_costs_month': {"text": "Try >> ibmcloud billing account-usage [-d YYYY-MM]"}
               }

    if intent in intents:
        data = intents[intent]

    # elif intent == "tar-directory-to-file":
    #     flags = "c{}f".format(flags)
    #     data = {"text": "Try >> tar -{} {} {}".format(flags, filename, dirname)}
    #
    # elif intent == "untar-file-to-directory":
    #     flags = "x{}f".format(flags)
    #     if 'directory-name' in entities:
    #         data = {"text": "Try >> tar -{} {} -C {}".format(flags, filename, dirname)}
    #     else:
    #         data = {"text": "Try >> tar -{} {}".format(flags, filename)}
    #
    # elif intent == "untar-group-of-files":
    #     flags = "x{}f".format(flags)
    #     ext = []
    #
    #     if 'file-extension' in entities:
    #         ext += entities['file-extension']
    #     elif 'file-type' in entities:
    #         ext += extensions[entities['file-type'][0]]
    #
    #     if not ext:
    #         ext = [".ext"]
    #
    #     if 'directory-name' in entities:
    #         data = {"text": "Try >> tar -{} {} --wildcards {} -C {}".format(flags, filename,
    #                                                                        ' '.join(["*" + e for e in ext]),
    #                                                                        dirname)}
    #     else:
    #         data = {
    #             "text": "Try >> tar -{} {} --wildcards {}".format(flags, filename, ' '.join(["*" + e for e in ext]))}
    #
    # elif intent == "untar-single-file":
    #     flags = "x{}f".format(flags)
    #
    #     if 'directory-name' in entities:
    #         data = {"text": "Try >> tar -{} {} -C {}".format(flags, filename, dirname)}
    #     else:
    #         data = {"text": "Try >> tar -{} {}".format(flags, filename)}
    #
    # elif intent == "add-to-file":
    #     flags = "{}rf".format(flags)
    #
    #     if 'tar-type' in entities:
    #         if "gz" in entities['tar-type'] or "bz2" in entities['tar-type']:
    #             data = {
    #                 "text": "The tar command don’t have a option to add files or directories to an existing "
    #                         "compressed tar.gz and tar.bz2 archive file."}
    #         else:
    #             data = {"text": "Unrecognized option."}
    #
    #     else:
    #         data = {"text": "Try >> tar -{} {} <file>".format(flags, filename)}
    #
    # elif intent == "list-contents":
    #
    #     flags = "{}tf".format(flags)
    #     ext = []
    #
    #     if 'file-extension' in entities:
    #         ext += entities['file-extension']
    #     elif 'file-type' in entities:
    #         ext += extensions[entities['file-type'][0]]
    #
    #     if not ext:
    #         data = {"text": "Try >> tar -{} {}".format(flags, filename)}
    #     else:
    #         data = {"text": "Try >> tar -{} {} '{}'".format(flags, filename, ' '.join(["*" + e for e in ext]))}

    else: pass

    return data, confidence




