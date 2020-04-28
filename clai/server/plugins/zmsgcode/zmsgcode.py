#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os
import re
import subprocess
from pathlib import Path
from typing import List

from clai.tools.colorize_console import Colorize

from clai.server.searchlib import Datastore
from clai.server.agent import Agent
from clai.server.command_message import State, Action, NOOP_COMMAND

from clai.server.logger import current_logger as logger

# Define constant strings for regular expressions
REGEX_ZMSG:str = "([A-Z]{3,}[0-9]{2,}[A,D,E,I,W,R]{0,1})[:]?\s?(.*$)"
REGEX_BPX:List[str] = [
    "^.*FAILED WITH RC=[0-9A-F]{1,4},\s*RSN=([0-9A-F]{7,8})\s*.*$",
    "errno2=0x([0-9A-Z]{8})",
    "0x([0-9A-Z]{8})"
]
REGEX_BPX_BADANSWER:List[str] = [
    "BPXMTEXT does not support reason code qualifier [0-9A-Z]{1,8}\\n",
    "[0-9]{1,8}\([0-9A-F]{1,8}x\) \\n"
]


class MsgCodeAgent(Agent):
    def __init__(self):
        super(MsgCodeAgent, self).__init__()
        inifile_path = os.path.join(str(Path(__file__).parent.absolute()), 'config.ini')
        self.store = Datastore(inifile_path)

    def compute_simple_token_similarity(self, src_sequence, tgt_sequence):
        src_tokens = set([x.lower().strip() for x in src_sequence.split()])
        tgt_tokens = set([x.lower().strip() for x in tgt_sequence.split()])

        return len(src_tokens & tgt_tokens) / len(src_tokens)

    def get_next_action(self, state: State) -> Action:
        return Action(suggested_command=state.command)

    def post_execute(self, state: State) -> Action:

        logger.info("==================== In zMsgCode Bot:post_execute ============================")
        logger.info("State:\n\tCommand: {}\n\tError Code: {}\n\tStderr: {}".format(state.command,
                                                                                   state.result_code,
                                                                                   state.stderr))
        logger.info("============================================================================")
        
        if state.result_code == '0':
            return Action(suggested_command=state.command)
        
        # This bot should be triggered if the message on STDERR resembles an
        # IBM z Systems message ID.  For example:
        #   FSUM8977 cp: source "test.txt" and target "test.txt" are identical
        #
        # If if the contents of state.stderr don't include a Z message code, move along
        matches = re.compile(REGEX_ZMSG).match(state.stderr)
        if matches is None:
            return Action(suggested_command=state.command)
        
        logger.info(f"Analyzing error message '{matches[0]}'")
        helpWasFound = False
        
        # Check all possible regexes for ID'ing a bpxmtext-able message
        bpx_matches = None
        for regex in REGEX_BPX:
            this_match = re.compile(regex).match(matches[0])
            if this_match is not None:
                bpx_matches = this_match
                break
        
        # If this message contains data which can be parsed by bpxmtext, then
        # try calling bpxmtext to get a string describing the error
        if bpx_matches is not None:
            reason_code:str = bpx_matches[1]
            logger.info(f"==> Reason Code: {reason_code}")
            
            # Call bpmxtext to get info about that message
            result:CompletedProcess = subprocess.run(["bpxmtext", reason_code], stdout=subprocess.PIPE)
            if result.returncode == 0:
                
                # Make sure our response from bpxmtext is useful
                bpxmtext_response_is_useful:bool = True
                for regex in REGEX_BPX_BADANSWER:
                    bad_answer = re.compile(regex).match(result.stdout)
                    if bad_answer is not None:
                        bpxmtext_response_is_useful = False
                        break
                
                if bpxmtext_response_is_useful:
                    logger.info(f"==> Success!!! Found bpxmtext info for code {reason_code}")
                    suggested_command=state.command
                    description=Colorize() \
                        .emoji(Colorize.EMOJI_ROBOT) \
                        .append(f"I asked bpxmtext about that message:") \
                        .info() \
                        .append(result.stdout.decode('UTF8')) \
                        .warning() \
                        .to_console()
                    helpWasFound = True # Mark that help was indeed found
            
        # If this message wasn't one we could send to bpxmtext, or if bpxmtext
        # didn't return a meaningful message, try searching the KnowledgeCenter
        if not helpWasFound:
            kc_api:Provider = self.store.getAPIs()['ibm_kc']
            if kc_api is not None and kc_api.canRunOnThisOS(): 
                msgid:str = matches[1]  # Isolate the message ID
                data = self.store.search(msgid, service='ibm_kc', size=1) 
                if data:
                    logger.info(f"==> Success!!! Found information for msgid {msgid}")
                    suggested_command=state.command
                    description=Colorize() \
                        .emoji(Colorize.EMOJI_ROBOT) \
                        .append(f"I looked up {msgid} in the IBM KnowledgeCenter for you:\n") \
                        .info() \
                        .append(kc_api.getPrintableOutput(data)) \
                        .warning() \
                        .to_console()
                    helpWasFound = True # Mark that help was indeed found
            
        if not helpWasFound:
            logger.info("Failure: Unable to be helpful")
            logger.info("============================================================================")
            
            suggested_command=NOOP_COMMAND
            description=Colorize().emoji(Colorize.EMOJI_ROBOT) \
                .append(
                    f"Sorry. It looks like you have stumbled across a problem that even the Internet doesn't have answer to.\n") \
                .info() \
                .append(f"Have you tried turning it OFF and ON again. ;)") \
                .to_console()
                
        return Action(suggested_command=suggested_command,
                      description=description,
                      confidence=1.0)
