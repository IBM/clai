#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from test_integration.contract_skills import ContractSkills


class TestSkillNlc2cmd(ContractSkills):
    def get_skill_name(self):
        return "nlc2cmd"

    def get_commands_to_execute(self):
        return [
            "show me how to add tags for ibmcloud",
            "show billing costs",
            "copy file to PDS member",
            "view mvs file",
            "extract files from an archive",
            'grep for all files with "clai" in this directory, show me details and line numbers',
        ]

    def get_commands_expected(self):
        return [
            "Try >> ibmcloud resource tag-attach --tag-names TAG --resource-name NAME",
            "Try >> ibmcloud billing account-usage [-d YYYY-MM]",
            "Try >> OGET [pathname] mvs_data_set_name(member_name)",
            "Try >> obrowse -r xx [file]",
            "Try >> tar -xf <archive-file>",
            'Try >> grep -rnv "clai" <directory>',
        ]
