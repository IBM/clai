#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from test_integration.contract_skills import ContractSkills


class TestSkillManPageExplorer(ContractSkills):

    def is_auto_mode(self):
        return False

    def get_skill_name(self):
        return 'man page explorer'

    def get_commands_to_execute(self):
        return ['pwd', 'clear screen?']

    def get_commands_expected(self):
        return ['/opt/IBM/clai', 'man clear']
