#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import unittest

from clai.server.command_message import NOOP_COMMAND, State
from clai.server.plugins.nlc2cmd.nlc2cmd import NLC2CMD


class NLC2CMDCloudTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = State(
            user_name="tester",
            command_id="0",
            command="show me the list of cloud tags",
            result_code="0",
        )

        cls.agent = NLC2CMD()

    # Checking login command
    @unittest.skip("Local dev testing only")
    def test_get_next_action_cloud_login(self):
        self.state.command = "how do i login"
        action = self.agent.get_next_action(state=self.state)
        print("Input: {}".format(self.state.command))
        print("---------------------------")
        print("Explanation: {}".format(action.description))
        self.assertEqual(NOOP_COMMAND, action.suggested_command)
        self.assertEqual("\x1b[95mTry >> ibmcloud login\x1b[0m", action.description)
        print("===========================")

    # Checking help command
    @unittest.skip("Local dev testing only")
    def test_get_next_action_cloud_help(self):
        self.state.command = "help me"
        action = self.agent.get_next_action(state=self.state)
        print("Input: {}".format(self.state.command))
        print("---------------------------")
        print("Explanation: {}".format(action.description))
        self.assertEqual(NOOP_COMMAND, action.suggested_command)
        self.assertEqual(
            "\x1b[95mTry >> ibmcloud help COMMAND\x1b[0m", action.description
        )
        print("===========================")

    # Checking invite command
    @unittest.skip("Local dev testing only")
    def test_get_next_action_cloud_invite(self):
        self.state.command = "I want to invite someone to my cloud"
        action = self.agent.get_next_action(state=self.state)
        print("Input: {}".format(self.state.command))
        print("---------------------------")
        print("Explanation: {}".format(action.description))
        self.assertEqual(NOOP_COMMAND, action.suggested_command)
        self.assertEqual(
            "\x1b[95mTry >> ibmcloud account user-invite USER_EMAIL\x1b[0m",
            action.description,
        )
        print("===========================")
