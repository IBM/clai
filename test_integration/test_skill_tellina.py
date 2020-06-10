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
        return ['print top 10 lines in a file',
                'show all files']

    def get_commands_expected(self):
    	# TODO: Fix workaround to the tellina 0.0 confidence issue
        return ['Try >> OGET [pathname] mvs_data_set_name(member_name)',
                'Try >> tar -xf <archive-file>']
