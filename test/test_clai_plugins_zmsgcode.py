#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os
import unittest
import tempfile

from subprocess import CompletedProcess
import subprocess

from builtins import classmethod
from typing import List

from clai.server.command_message import State, Action
from clai.server.plugins.zmsgcode.zmsgcode import MsgCodeAgent
from clai.tools.colorize_console import Colorize

OS_NAME: str = os.uname().sysname.upper()

@unittest.skipIf(OS_NAME not in ("OS/390", "Z/OS"), "Test only valid on z/OS")
class MsgCodeAgentTest(unittest.TestCase):
    @classmethod
    def set_up_class(cls):
        _agent = MsgCodeAgent()
        cls.agent = _agent

    @classmethod
    def try_command(cls, command_and_args: List[str]) -> Action:
        result: CompletedProcess = subprocess.run(
            command_and_args,
            encoding='UTF8',
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Gather command response information needed for State object
        command: str = None
        if isinstance(result.args, list):
            command = ' '.join(result.args)
        else:
            command = result.args
        result_code: str = str(result.returncode)

        return cls.scaffold_command_response(command=command,
                                             result_code=result_code,
                                             stdout=result.stdout,
                                             stderr=result.stderr)

    @classmethod
    def scaffold_command_response(cls, **kwargs) -> Action:
        state = State(
            command_id='0',
            user_name='tester',
            command=kwargs['command'],
            result_code=kwargs['result_code'],
            stderr=kwargs['stderr'])

        print(f"Command: {kwargs['command']}")
        print(f"RetCode: {kwargs['result_code']}")
        print(f"stdout: '{kwargs['stdout']}'")
        print(f"stderr: '{kwargs['stderr']}'")
        print("===========================")

        #action = cls.agent.get_next_action(state=state)
        action = cls.agent.post_execute(state=state)

        print("Input: {}".format(state.command))
        print("===========================")
        print("Response: {}".format(action.suggested_command))
        print("===========================")
        print("Explanation: {}".format(action.description))

        return action

    @unittest.skip("Only for local testing")
    def test_bpxmtextable_message_bad_cd(self):
        self.agent.init_agent()

        with tempfile.NamedTemporaryFile() as our_file:
            action = self.try_command(["cd", our_file.name])
        lines = action.description.strip().split('\n')
        self.assertEqual(f"{Colorize.EMOJI_ROBOT}I asked bpxmtext about that message:", lines[0])
        self.assertEqual("Action: Reissue the service specifying a directory file.", lines[-2])

    @unittest.skip("Only for local testing")
    def test_bpxmtextable_message_bad_cat(self):
        self.agent.init_agent()

        with tempfile.NamedTemporaryFile() as our_file:
            file_that_isnt_there: str = our_file.name
        action = self.try_command(["cat", file_that_isnt_there])
        lines = action.description.strip().split('\n')
        self.assertEqual(f"{Colorize.EMOJI_ROBOT}I asked bpxmtext about that message:", lines[0])
        self.assertEqual("Action: The open service request cannot be processed. Correct the name or the", lines[-3])
        self.assertEqual("open flags and retry the operation.", lines[-2])

    @unittest.skip("Only for local testing")
    def test_bpxmtextable_unhelpful_message_1(self):
        self.agent.init_agent()

        action = self.scaffold_command_response(
            command=["not", "a", "real", "command"],
            result_code=str(1),
            stdout="",
            stderr="IEB4223I 0xDFDFDFDF"
        )

        lines = action.description.strip().split('\n')
        self.assertEqual(f"{Colorize.EMOJI_ROBOT}I couldn't find any help for message code 'IEB4223I'", lines[0])

    @unittest.skip("Only for local testing")
    def test_bpxmtextable_unhelpful_message_2(self):
        self.agent.init_agent()

        action = self.scaffold_command_response(
            command=["not", "a", "real", "command"],
            result_code=str(1),
            stdout="",
            stderr="IEB4223I 0xDFDF"
        )

        lines = action.description.strip().split('\n')
        self.assertEqual(f"{Colorize.EMOJI_ROBOT}I couldn't find any help for message code 'IEB4223I'", lines[0])

    @unittest.skip("Only for local testing")
    def test_bad_cp(self):
        self.agent.init_agent()

        with tempfile.NamedTemporaryFile() as our_file:
            action = self.try_command(["cp", our_file.name, our_file.name])
        lines = action.description.strip().split('\n')
        self.assertEqual(f"{Colorize.EMOJI_ROBOT}I looked up FSUM8977 in the IBM KnowledgeCenter for you:", lines[0])
        self.assertEqual(f"{Colorize.INFO}Product: z/OS", lines[1])
        self.assertEqual("Topic: FSUM8977 ...", lines[2])
