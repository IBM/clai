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
wa_endpoint = 'https://ibmcloud-helper.mybluemix.net/message'

def wa_skill_processor_cloudbot(msg):

    # Confidence remains at 0 unless an intent has been detected
    confidence = 0.0 

    # Make sure we are not intercepting real IBM Cloud CLI commands
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
        intent = "ibmcloud help"

    intents = { 'add_tag_resource': {"text": "Try >> ibmcloud resource tag-attach --tag-names TAG --resource-name NAME"},
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
                'view_usage_costs_month': {"text": "Try >> ibmcloud billing account-usage [-d YYYY-MM]"}}

    if intent in intents: data = intents[intent]
    else: pass

    return data, confidence


while True:

    ip = input('>> ')

    if ip == 'exit': break
    else: print(wa_skill_processor_cloudbot(str(ip).strip()))



