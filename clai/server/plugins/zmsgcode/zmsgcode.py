#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os
import re
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

    def compute_confidence(self, query, forum, manpage):
        """
        Computes the confidence based on query, stack-exchange post answer and manpage

        Algorithm:
            1. Compute token-wise similarity b/w query and forum text
            2. Compute token-wise similarity b/w forum text and manpage description
            3. Return product of two similarities


        Args:
            query (str): standard error captured in state variable
            forum (str): answer text from most relevant stack exchange post w.r.t query
            manpage (str): manpage description for most relevant manpage w.r.t. forum

        Returns:
             confidence (float): confidence on the returned manpage w.r.t. query
        """
        query_forum_similarity = self.compute_simple_token_similarity(query, forum[0]['Content'])
        forum_manpage_similarity = self.compute_simple_token_similarity(forum[0]['Answer'], manpage)
        confidence = query_forum_similarity * forum_manpage_similarity
        return confidence

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
        
        # See if the contents of state.stderr match that of a z/OS message
        helpWasFound = False
        matches = zmessage.match(re.escape(state.stderr))
        if(matches is not None):
            # Use the KnowledgeCenter provider to look up information on this msgid
            kc_api:Provider = self.store.getAPIs()['ibm_kc']
            
            # Only do this if the KnowledgeCenter API can run on this OS
            if kc_api is not None and kc_api.canRunOnThisOS(): 
                # Isolate the message ID
                msgid:str = matches[1]
                
                data = self.store.search(msgid, service='ibm_kc', size=1) 
                if data:
                    logger.info(f"==> Success!!! Found information for msgid {msgid}")
    
                    # Find closest match b/w relevant data and manpages for unix
                    searchResult = kc_api.extractSearchResult(data)
                    manpages = self.store.search(searchResult, service='manpages', size=5)
                    if manpages:
                        logger.info("==> Success!!! found relevant manpages.")
    
                        command = manpages['commands'][-1]
                        confidence = manpages['dists'][-1]
    
                        # FIXME: Artificially boosted confidence
                        confidence = 1.0
    
                        logger.info("==> Command: {} \t Confidence:{}".format(command, confidence))
                        
                        # Set return data
                        suggested_command="man {}".format(command)
                        description=Colorize() \
                            .emoji(Colorize.EMOJI_ROBOT).append(f"I did little bit of Internet searching for you, ") \
                            .append(f"and found this in the {kc_api}:\n") \
                            .info() \
                            .append(kc_api.getPrintableOutput(data)) \
                            .warning() \
                            .append("Do you want to try: man {}".format(command)) \
                            .to_console()
                        
                        # Mark that help was indeed found
                        helpWasFound = True
                
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
            confidence=0.0
                
        return Action(suggested_command=suggested_command,
                      description=description,
                      confidence=confidence)
