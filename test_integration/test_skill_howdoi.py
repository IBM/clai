#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from test_integration.contract_skills import ContractSkills


class TestSkillHowDoI(ContractSkills):
    def is_auto_mode(self):
        return False

    def get_skill_name(self):
        return "howdoi"

    def get_commands_to_execute(self):
        return [
            "pwd",
            'clai "howdoi" when to use sudo vs su?',
            'clai "howdoi" find out disk usage per user?',
            'clai "howdoi" How to process gz files?',
        ]

    def get_commands_expected(self):
        return ["/opt/IBM/clai", "su", "df", "gzip"]
