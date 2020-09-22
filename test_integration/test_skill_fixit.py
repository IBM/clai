#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from test_integration.contract_skills import ContractSkills


class TestSkillFixit(ContractSkills):
    def get_skill_name(self):
        return "fixit"

    def get_commands_to_execute(self):
        return ["clean", "puthon"]

    def get_commands_expected(self):
        return ["clear", "python"]
