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

        intent = "generic"
        confidence = 0.0

    intents = { 'add_tag_resource'                 : "resource tag-attach --tag-names TAG --resource-name NAME",
                'assign_access_create_policy'      : "iam user-policy-create USER_NAME [OPTIONS]",
                'create_access_group'              : "iam user-policy-create USER_NAME [OPTIONS]",
                'create_api_key'                   : "iam api-key-create NAME -d DESCRIPTION",
                'create_org_cloudfoundry_services' : "account org-create ORG_NAME",
                'create_resource'                  : "resource service-instance-create NAME SERVICE_NAME PLAN_NAME LOCATION",
                'create_resource_group'            : "resource group create GROUP_NAME",
                'create_space_services_org'        : "account space-create SPACE_NAME",
                'install_plugin'                   : "plugin install NAME",
                'invite_user_to_account'           : "account user-invite USER_EMAIL",
                'list_plugins'                     : "plugin repo-plugins",
                'list_services_resource_group'     : "resource service-instances -g GROUP_NAME",
                'list_tags_account'                : "resource tags",
                'list_users_in_account'            : "account users (works only for account owners)",
                'search_ibm_cloud_catalog'         : "catalog search QUERY",
                'target_cloudfoundry_org'          : "target --cf",
                'view_service_details'             : "catalog service NAME",
                'view_usage_costs_month'           : "billing account-usage [-d YYYY-MM]",
                'login'                            : "login",
                'help'                             : "help COMMAND",
                'generic'                          : "help" }

    data = { "text" : "Try >> ibmcloud " + intents[intent] } 
    return data, confidence

