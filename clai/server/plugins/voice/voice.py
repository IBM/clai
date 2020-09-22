#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os
import tempfile
import subprocess

from clai.server.agent import Agent
from clai.server.command_message import Action, State, NOOP_COMMAND

from gtts import gTTS


class Voice(Agent):
    def __init__(self):
        super(Voice, self).__init__()
        self._tmp_filepath = os.path.join(tempfile.gettempdir(), "tts.mp3")

    # pylint: disable=no-self-use
    def summarize_output(self, state):
        cmd = str(state.command)
        stderr = str(state.stderr)
        err_txt = stderr.split("\n")[0]  # Speak the first line

        text = f"Error occurred for command {cmd}. " f"Error is: {err_txt}"

        return text

    def synthesize(self, text):
        """ Converts text to audio and saves to temp file """
        tts = gTTS(text, lang="en", lang_check=False)
        tts.save(self._tmp_filepath)

    def speak(self):
        subprocess.Popen(
            [
                "nohup",
                "ffplay",
                "-nodisp",
                "-autoexit",
                "-nostats",
                "-hide_banner",
                "-loglevel",
                "warning",
                self._tmp_filepath,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def post_execute(self, state: State) -> Action:

        if state.result_code == "0":
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
