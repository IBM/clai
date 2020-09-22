#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from test_integration.contract_skills import ContractSkills


class TestSkillHelpme(ContractSkills):

    def get_skill_name(self):
        return 'helpme'

    def get_commands_to_execute(self):
        return ['pwd', 'apt-get install emacs']

    def get_commands_expected(self):
        return ['/opt/IBM/clai', 'apt']
