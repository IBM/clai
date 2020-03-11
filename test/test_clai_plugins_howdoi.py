#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import unittest

from clai.server.command_message import State
from clai.server.plugins.howdoi.howdoi import HowDoIAgent


class SearchAgentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _agent = HowDoIAgent()
        cls.agent = _agent

    @unittest.skip("Only for local testing")
    def test_get_next_action_pwd_without_question(self):
        self.agent.init_agent()

        state = State(user_name='tester', command_id='0', command="pwd")
        action = self.agent.get_next_action(state=state)
        print("Input: {}".format(state.command))
        print("===========================")
        print("Response: {}".format(action.suggested_command))
        print("===========================")
        print("Explanation: {}".format(action.description))
        self.assertEqual('pwd', action.suggested_command)

    @unittest.skip("Only for local testing")
    def test_get_next_action_pwd_with_question(self):
        self.agent.init_agent()

        state = State(user_name='tester', command_id='0', command="What is pwd?")
        action = self.agent.get_next_action(state=state)
        print("Input: {}".format(state.command))
        print("===========================")
        print("Response: {}".format(action.suggested_command))
        print("===========================")
        print("Explanation: {}".format(action.description))
        self.assertEqual('man pwd', action.suggested_command)

    @unittest.skip("Only for local testing")
    def test_get_next_action_sudo(self):
        self.agent.init_agent()

        state = State(user_name='tester', command_id='0', command="when to use sudo vs su?")
        action = self.agent.get_next_action(state=state)
        print("Input: {}".format(state.command))
        print("===========================")
        print("Response: {}".format(action.suggested_command))
        print("===========================")
        print("Explanation: {}".format(action.description))
        self.assertEqual('man su', action.suggested_command)

    @unittest.skip("Only for local testing")
    def test_get_next_action_disk(self):
        self.agent.init_agent()

        state = State(user_name='tester', command_id='0', command="find out disk usage per user?")
        action = self.agent.get_next_action(state=state)
        print("Input: {}".format(state.command))
        print("===========================")
        print("Response: {}".format(action.suggested_command))
        print("===========================")
        print("Explanation: {}".format(action.description))
        self.assertEqual('man df', action.suggested_command)

    @unittest.skip("Only for local testing")
    def test_get_next_action_zip(self):
        self.agent.init_agent()

        state = State(user_name='tester', command_id='0', command="How to process gz files?")
        action = self.agent.get_next_action(state=state)
        print("Input: {}".format(state.command))
        print("===========================")
        print("Response: {}".format(action.suggested_command))
        print("===========================")
        print("Explanation: {}".format(action.description))
        self.assertEqual('man gzip', action.suggested_command)
