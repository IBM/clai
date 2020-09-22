#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import unittest

from clai.server.command_message import State, NOOP_COMMAND
from clai.server.plugins.helpme.helpme import HelpMeAgent


class RetrievalAgentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.state = State(
            user_name="tester",
            command_id="0",
            command="./tmp_file.sh",
            result_code="1",
            stderr="Permission denied",
        )

        cls.agent = HelpMeAgent()

    @unittest.skip("Need internet connection")
    def test_get_post_execute(self):
        action = self.agent.post_execute(state=self.state)
        print("Input: {}".format(self.state.command))
        print("===========================")
        print("Response: {}".format(action.suggested_command))
        print("===========================")
        print("Explanation: {}".format(action.description))
        self.assertNotEqual(NOOP_COMMAND, action.suggested_command)

    @unittest.skip("Local testing")
    def test_get_forum(self):
        forum = self.agent.store.search(
            "Permission denied", service="stack_exchange", size=1
        )
        self.assertEqual(1, len(forum))

    @unittest.skip("Local testing")
    def test_get_KnowledgeCenter(self):
        kc_hits = self.agent.store.search("Permission denied", service="ibm_kc", size=1)
        print("Got this result from the KnowledgeCenter: " + str(kc_hits))
        self.assertEqual(1, len(kc_hits))

        man_hits = self.agent.store.search(
            kc_hits[0]["summary"], service="manpages", size=10
        )

        print("Got this result from the Manpages service: " + str(man_hits))
        self.assertEqual("connect", man_hits["commands"][-1])

    @unittest.skip("Local testing")
    def test_get_command(self):
        hits = self.agent.store.search(
            "sudo allows a permitted user to execute a command"
            "as the superuser or another user, as specified "
            "by the security policy.  The invoking user's real "
            "(not effective) user ID is used to determine the "
            "user name with which to query the "
            "security policy.",
            service="manpages",
            size=10,
        )

        self.assertEqual("sudo", hits["commands"][-1])
