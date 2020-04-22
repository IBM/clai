#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os
import sys
import unittest

from clai.server.command_message import State
from clai.server.plugins.howdoi.howdoi import HowDoIAgent
from builtins import classmethod

OS_NAME:str = os.uname().sysname.lower()


#@unittest.skip("Only for local testing")
class SearchAgentTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        _agent = HowDoIAgent()
        cls.agent = _agent
        
    @classmethod
    def getQandA(cls):
        question:str = ""
        answer:str = ""
        
        callerFrame = sys._getframe(2) if hasattr(sys, "_getframe") else None
        if callerFrame is not None:
            method:str = callerFrame.f_code.co_name
            
            if method == "test_get_next_action_pwd_without_question":
                if OS_NAME == "OS/390":
                    question = "pds"
                    answer = "pds"
                else:
                    question = "pwd"
                    answer = None
            
            elif method == "test_get_next_action_pwd_with_question":
                if OS_NAME == "OS/390":
                    question = "What is a pds?"
                    answer = "man dde"
                else:
                    question = "What is pwd?"
                    answer = "man pwd"
            
            elif method == "test_get_next_action_sudo":
                question = "when to use sudo vs su?"
                if OS_NAME == "OS/390":
                    answer = "man ssh"
                else:
                    answer = "man su"
            
            elif method == "test_get_next_action_disk":
                question = "find out disk usage per user?"
                if OS_NAME == "OS/390":
                    answer = "man perlopentut"
                else:
                    answer = "man df"
            
            elif method == "test_get_next_action_zip":
                question = "How to process gz files?"
                if OS_NAME == "OS/390":
                    answer = "man dnctl"
                else:
                    answer = "man gzip"
            
            elif method == "test_get_next_action_pds":
                question = "copy a PDS member?"
                if OS_NAME == "OS/390":
                    answer = "man rpc.h"
                else:
                    answer = "man cmp"
        
        return(question, answer)

    #@unittest.skip("Only for local testing")
    def test_get_next_action_pwd_without_question(self):
        self.agent.init_agent()
        question, answer = self.getQandA()

        state = State(user_name='tester', command_id='0', command=question)
        action = self.agent.get_next_action(state=state)
        print("Input: {}".format(state.command))
        print("===========================")
        print("Response: {}".format(action.suggested_command))
        print("===========================")
        print("Explanation: {}".format(action.description))
        self.assertEqual(answer, action.suggested_command)

    #@unittest.skip("Only for local testing")
    def test_get_next_action_pwd_with_question(self):
        self.agent.init_agent()
        question, answer = self.getQandA()

        state = State(user_name='tester', command_id='0', command=question)
        action = self.agent.get_next_action(state=state)
        print("Input: {}".format(state.command))
        print("===========================")
        print("Response: {}".format(action.suggested_command))
        print("===========================")
        print("Explanation: {}".format(action.description))
        self.assertEqual(answer, action.suggested_command)

    #@unittest.skip("Only for local testing")
    def test_get_next_action_sudo(self):
        self.agent.init_agent()
        question, answer = self.getQandA()

        state = State(user_name='tester', command_id='0', command=question)
        action = self.agent.get_next_action(state=state)
        print("Input: {}".format(state.command))
        print("===========================")
        print("Response: {}".format(action.suggested_command))
        print("===========================")
        print("Explanation: {}".format(action.description))
        self.assertEqual(answer, action.suggested_command)

    #@unittest.skip("Only for local testing")
    def test_get_next_action_disk(self):
        self.agent.init_agent()
        question, answer = self.getQandA()

        state = State(user_name='tester', command_id='0', command=question)
        action = self.agent.get_next_action(state=state)
        print("Input: {}".format(state.command))
        print("===========================")
        print("Response: {}".format(action.suggested_command))
        print("===========================")
        print("Explanation: {}".format(action.description))
        self.assertEqual(answer, action.suggested_command)

    #@unittest.skip("Only for local testing")
    def test_get_next_action_zip(self):
        self.agent.init_agent()
        question, answer = self.getQandA()

        state = State(user_name='tester', command_id='0', command=question)
        action = self.agent.get_next_action(state=state)
        print("Input: {}".format(state.command))
        print("===========================")
        print("Response: {}".format(action.suggested_command))
        print("===========================")
        print("Explanation: {}".format(action.description))
        self.assertEqual(answer, action.suggested_command)
    
    #@unittest.skip("Only for local testing")
    def test_get_next_action_pds(self):
        self.agent.init_agent()
        question, answer = self.getQandA()

        state = State(user_name='tester', command_id='0', command=question)
        action = self.agent.get_next_action(state=state)
        print("Input: {}".format(state.command))
        print("===========================")
        print("Response: {}".format(action.suggested_command))
        print("===========================")
        print("Explanation: {}".format(action.description))
        self.assertEqual(answer, action.suggested_command)
