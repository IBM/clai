#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os
import unittest
import tempfile

from clai.server.command_message import State
from clai.server.plugins.zmsgcode.zmsgcode import MsgCodeAgent
from builtins import classmethod

OS_NAME:str = os.uname().sysname.lower()

class MsgCodeAgentTestException(Exception):
    def __init__(self, method:str):
        Exception.__init__(
            self,
            f"The 'command' parameter is required when called from {method}()"
        )

@unittest.skip("Only for local testing")
class MsgCodeAgentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _agent = MsgCodeAgent()
        cls.agent = _agent
    
    @unittest.skip("Only for local testing")
    def test_bpxmtextable_message(self):
        self.agent.init_agent()
        
        with tempfile.NamedTemporaryFile() as f:
            state = State(user_name='tester', command_id='0', command=f"cd {f.name} {f.name}")
            action = self.agent.get_next_action(state=state)
            print("Input: {}".format(state.command))
            print("===========================")
            print("Response: {}".format(action.suggested_command))
            print("===========================")
            print("Explanation: {}".format(action.description))
            self.assertEqual("bob", action.suggested_command)