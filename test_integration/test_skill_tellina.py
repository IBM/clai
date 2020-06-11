#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from test_integration.contract_skills import ContractSkills


class TestSkillTellina(ContractSkills):

    def get_skill_name(self):
        return 'tellina'

    def get_commands_to_execute(self):
        skill_name = self.get_skill_name()
        return ['pwd',
                f'clai "{skill_name}" exit terminal',
                f'clai "{skill_name}" show me all files']

    def get_commands_expected(self):
        return ['/opt/IBM/clai',
                'exit',
                'find .']
 