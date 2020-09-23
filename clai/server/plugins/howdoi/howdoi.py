#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import os
from pathlib import Path

from clai.tools.colorize_console import Colorize

from clai.server.searchlib.data import Datastore
from clai.server.agent import Agent
from clai.server.command_message import State, Action, NOOP_COMMAND
from clai.server.plugins.howdoi.question_detection import QuestionDetection

from clai.server.logger import current_logger as logger


class HowDoIAgent(Agent):
    def __init__(self):
        super(HowDoIAgent, self).__init__()
        inifile_path = os.path.join(str(Path(__file__).parent.absolute()), 'config.ini')
        self.store = Datastore(inifile_path)
        self.questionIdentifier = QuestionDetection()

    def compute_simple_token_similarity(self, src_sequence, tgt_sequence):
        src_tokens = set([x.lower().strip() for x in src_sequence.split()])
        tgt_tokens = set([x.lower().strip() for x in tgt_sequence.split()])

        return len(src_tokens & tgt_tokens) / len(src_tokens)

    def get_next_action(self, state: State) -> Action:

        logger.info("================== In HowDoI Bot:get_next_action ========================")
        logger.info("State:\n\tCommand: {}\n\tError Code: {}\n\tStderr: {}".format(state.command,
                                                                                   state.result_code,
                                                                                   state.stderr))
        logger.info("============================================================================")

        # Invoke "howdoi" plugin only when a question is asked
        is_question = self.questionIdentifier.is_question(state.command)

        if not is_question:
            return Action(
                suggested_command=state.command,
                confidence=0.0
            )
        
        apis:OrderedDict=self.store.get_apis()
        helpWasFound = False
        for provider in apis:
            # We don't want to process the manpages provider... thats the provider
            # that we use to clarify results from other providers
            if provider == "manpages":
                logger.info(f"Skipping search provider 'manpages'")
                continue
            
            thisAPI:Provider = apis[provider]
            
            # Skip this provider if it isn't supported on the target OS
            if not thisAPI.can_run_on_this_os():
                logger.info(f"Skipping search provider '{provider}'")
                logger.info(f"==> Excluded on platforms: {str(thisAPI.get_excludes())}")
                continue # Move to next provider in list
            
            logger.info(f"Processing search provider '{provider}'")
            
            if thisAPI.has_variants():
                logger.info(f"==> Has search variants: {str(thisAPI.get_variants())}")
                variants:List = thisAPI.get_variants()
            else:
                logger.info(f"==> Has no search variants")
                variants:List = [None]
            
            # For each search variant supported by the current API, query
            # the data store to find the closest matching data.  If there are
            # no search variants (ie: the singleton variant case), the variants
            # list will only contain a single, Nonetype value.
            for variant in variants:
        
                if variant is not None:
                    logger.info(f"==> Searching variant '{variant}'")
                    data = self.store.search(state.command, service=provider, size=1, searchType=variant)
                else:
                    data = self.store.search(state.command, service=provider, size=1)
                    
                if data:
                    logger.info(f"==> Success!!! Found a result in the {thisAPI}")
    
                    # Find closest match b/w relevant data and manpages for unix
                    searchResult = thisAPI.extract_search_result(data)
                    manpages = self.store.search(searchResult, service='manpages', size=5)
                    if manpages:
                        logger.info("==> Success!!! found relevant manpages.")
        
                        command = manpages['commands'][-1]
                        confidence = manpages['dists'][-1]
        
                        logger.info("==> Command: {} \t Confidence:{}".format(command, confidence))
                        
                        # Set return data
                        suggested_command="man {}".format(command)
                        description=Colorize() \
                            .emoji(Colorize.EMOJI_ROBOT).append(f"I did little bit of Internet searching for you, ") \
                            .append(f"and found this in the {thisAPI}:\n") \
                            .info() \
                            .append(thisAPI.get_printable_output(data)) \
                            .warning() \
                            .append("Do you want to try: man {}".format(command)) \
                            .to_console()
                        
                        # Mark that help was indeed found
                        helpWasFound = True
                        
                        # We've found help; no need to keep searching
                        break
                
            # If we found help, then break out of the outer loop as well
            if helpWasFound:
                break
            
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
