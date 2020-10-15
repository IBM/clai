#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os
import unittest

from builtins import classmethod

from clai.server.command_message import State
from clai.server.plugins.howdoi.howdoi import HowDoIAgent

OS_NAME: str = os.uname().sysname.upper()


# @unittest.skip("Only for local testing")
class SearchAgentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _agent = HowDoIAgent()
        cls.agent = _agent

    def print_and_verify(self, question, answer):
        state = State(user_name="tester", command_id="0", command=question)
        action = self.agent.get_next_action(state=state)
        print(f"Input: {state.command}")
        print("===========================")
        print(f"Response: {action.suggested_command}")
        print("===========================")
        print(f"Explanation: {action.description}")
        self.assertEqual(answer, action.suggested_command)

    @unittest.skip("Only for local testing")
    def test_get_next_action_pwd_without_question(self):
        self.agent.init_agent()
        if OS_NAME in ("OS/390", "Z/OS"):
            self.print_and_verify("pds", "pds")
        else:
            self.print_and_verify("pds", None)

    # @unittest.skip("Only for local testing")
    def test_get_next_action_pwd_with_question(self):
        self.agent.init_agent()
        if OS_NAME in ("OS/390", "Z/OS"):
            self.print_and_verify("What is a pds?", "man readlink")
        else:
            self.print_and_verify("What is pwd?", "man pwd")

    @unittest.skip("Only for local testing")
    def test_get_next_action_sudo(self):
        self.agent.init_agent()
        self.print_and_verify("when to use sudo vs su?", "man su")

    @unittest.skip("Only for local testing")
    def test_get_next_action_disk(self):
        self.agent.init_agent()
        question: str = "find out disk usage per user?"
        if OS_NAME in ("OS/390", "Z/OS"):
            self.print_and_verify(question, "man du")
        else:
            self.print_and_verify(question, "man df")

    @unittest.skip("Only for local testing")
    def test_get_next_action_zip(self):
        self.agent.init_agent()
        question: str = "How to process gz files?"
        if OS_NAME in ("OS/390", "Z/OS"):
            self.print_and_verify(question, "man dnctl")
        else:
            self.print_and_verify(question, "man gzip")

    @unittest.skip("Only for local testing")
    def test_get_next_action_pds(self):
        self.agent.init_agent()
        question: str = "copy a PDS member?"
        if OS_NAME in ("OS/390", "Z/OS"):
            self.print_and_verify(question, "man tcsh")
        else:
            self.print_and_verify(question, "man cmp")


if __name__ == "__main__":
    unittest.main()
