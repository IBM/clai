#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from test_integration.contract_skills import ContractSkills


class TestSkillNlc2cmd(ContractSkills):

    def get_skill_name(self):
        return 'nlc2cmd'

    def get_commands_to_execute(self):
        return ['compress this directory into a bz2 file',
                'extract files from an archive',
                'grep for all files with "clai" in this directory, show me details and line numbers']

    def get_commands_expected(self):
        return ['Try >> tar -cjf <archive-file> <directory>',
                'Try >> tar -xf <archive-file>',
                'Try >> grep -rnv "clai" <directory>']
