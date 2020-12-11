#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os
import json
import tempfile
import subprocess
from pathlib import Path

from clai.server.agent import Agent
from clai.server.command_message import Action, State, NOOP_COMMAND
from clai.server.utilities.gpt3.gpt3 import GPT, Example

from gtts import gTTS


class Voice(Agent):

    def __init__(self):
        super(Voice, self).__init__()

        self._api_filename = "openai_api.key"
        self._priming_filename = "priming.json"
        self._tmp_filepath = os.path.join(tempfile.gettempdir(), 'tts.mp3')

        self._gpt_api = self.__init_gpt_api__()
        self.__prime_gpt_model__()

    def __init_gpt_api__(self):
        curdir = str(Path(__file__).parent.absolute())
        key_filepath = os.path.join(curdir, self._api_filename)
        with open(key_filepath, 'r') as f:
            key = f.read()

        gpt_api = GPT()
        gpt_api.set_api_key(key)
        return gpt_api

    def __prime_gpt_model__(self):
        curdir = str(Path(__file__).parent.absolute())
        priming_filepath = os.path.join(curdir, self._priming_filename)
        with open(priming_filepath, 'r') as f:
            priming_examples = json.load(f)

        for priming_set in priming_examples:
            ip, op = priming_set['input'], priming_set['output']
            example = Example(ip, op)
            self._gpt_api.add_example(example)

    def summarize_output(self, state):
        stderr = str(state.stderr)
        prompt = stderr.split('\n')[0]
        gpt_summary = self._gpt_api.get_top_reply(prompt, strip_output_suffix=True)
        summary = f"error. {gpt_summary}"
        return summary

    def synthesize(self, text):
        """ Converts text to audio and saves to temp file """
        tts = gTTS(text, lang='en', lang_check=False)
        tts.save(self._tmp_filepath)

    def speak(self):
        subprocess.Popen(['nohup', 'ffplay', '-nodisp', '-autoexit',
                          '-nostats', '-hide_banner',
                          '-loglevel', 'warning', self._tmp_filepath],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def post_execute(self, state: State) -> Action:

        if state.result_code == '0':
            return Action(suggested_command=state.command)

        # Summarize output from current state
        text_to_speak = self.summarize_output(state)

        # Convert text to audio
        self.synthesize(text_to_speak)

        # Play the generated audio
        self.speak()

        return Action(suggested_command=NOOP_COMMAND, confidence=0.01)

    def get_next_action(self, state: State) -> Action:
        return Action(suggested_command=state.command)
