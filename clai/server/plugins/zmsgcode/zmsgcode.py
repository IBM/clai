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

from clai.tools.colorize_console import Colorize

from clai.server.searchlib import Datastore
from clai.server.agent import Agent
from clai.server.command_message import State, Action, NOOP_COMMAND

from clai.server.logger import current_logger as logger


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
        
        # This bot should be triggered if the message on STDERR resembles an
        # IBM z Systems message ID.  For example:
        #   FSUM8977 cp: source "test.txt" and target "test.txt" are identical
        zmessage = re.compile("(^[A-Z]{3,}[0-9]{2,}[A,D,E,I,W,R]{0,1})([:]?\s)(.*$)")
        bpxmsg = re.compile("^.*FAILED WITH RC=([0-9A-F]{1,4}),\s*RSN=([0-9A-F]{7,8})\s*.*$")
        bad_bpx_result_1 = re.compile("BPXMTEXT does not support reason code qualifier [0-9A-Z]{1,8}\\n")
        bad_bpx_result_2 = re.compile("[0-9]{1,8}\([0-9A-F]{1,8}x\) \\n")
        
        # See if the contents of state.stderr match that of a z/OS message
        matches = zmessage.match(state.stderr)
        if(matches is not None):
            logger.info(f"Analyzing error message '{matches[0]}'")
            helpWasFound = False
            
            # See if this message contains data which can be parse by bpxmtext.
            # If it does, we will use that. Otherwise, we will search the
            # IBM KnowledgeCenter for that information.
            bpx_matches = bpxmsg.match(matches[0])
            if bpx_matches is not None:
                return_code:str = bpx_matches[1]
                reason_code:str = bpx_matches[2]
                logger.info(f"==> Return Code: {return_code}")
                logger.info(f"==> Reason Code: {reason_code}")
                
                # Call bpmxtext to get info about that message
                result:CompletedProcess = subprocess.run(["bpxmtext", reason_code], stdout=subprocess.PIPE)
                
                # Make sure that we actually found something useful
                if result.returncode == 0 \
                and bad_bpx_result_1.match(result.stdout) is None \
                and bad_bpx_result_2.match(result.stdout) is None:
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
                
            # If we still haven't found any help, see if we can get some information
            # from the KnowledgeCenter documentation library
            if not helpWasFound:
                # Use the KnowledgeCenter provider to look up information on this msgid
                kc_api:Provider = self.store.getAPIs()['ibm_kc']
                
                # Only do this if the KnowledgeCenter API can run on this OS
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
        
        return Action(suggested_command=state.command, confidence=0.0)
