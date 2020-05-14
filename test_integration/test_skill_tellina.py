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
        return ['print two top commands',
                'extract files from an archive',
                'grep for all files with "clai" in this directory, show me details and line numbers']

    def get_commands_expected(self):
        return ['Try >> echo $( ls $( which top ) )',
                'Try >> tar -x -v -f $FILE',
                'Try >> find /usr/share/cli -name *cli*']
