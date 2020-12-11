#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.server.agent import Agent
from clai.server.command_message import State, Action, NOOP_COMMAND
from clai.tools.colorize_console import Colorize

from clai.server.utilities.gpt3.gpt3 import GPT, Example

from pathlib import Path
import json 
import os

class GPT3(Agent):
    def __init__(self):
        super(GPT3, self).__init__()
        self._gpt3_api = self.__init_gpt3_api__()

    def __init_gpt3_api__(self):

        current_directory = str(Path(__file__).parent.absolute())

        path_to_gpt3_key = os.path.join(current_directory, "openai_api.key")
        path_to_gpt3_prompts = os.path.join(current_directory, "prompt.json")

        gpt3_key = open(path_to_gpt3_key, 'r').read()
        gpt3_prompts = json.load(open(path_to_gpt3_prompts, 'r'))

        gpt3_api = GPT(temperature=0)
        gpt3_api.set_api_key(gpt3_key)

        for prompt in gpt3_prompts:
            ip, op = prompt['input'], prompt['output']
            example = Example(ip, op)
            gpt3_api.add_example(example)

        return gpt3_api

    def get_next_action(self, state: State) -> Action:

        # user typed in, in natural language
        command = state.command

        # truncate to first 1000 chars
        command = command[:1000]

        try:

            response = self._gpt3_api.get_top_reply(command, strip_output_suffix=True)
            response = response.strip()

            return Action(
                suggested_command=response,
                execute=False,
                description="Currently the GPT-3 skill does not provide an explanation. Got an idea? Contribute to CLAI!",
                confidence=0.0)

        except Exception as ex:
            return [ { "text" : "Method failed with status " + str(ex) }, 0.0 ]

