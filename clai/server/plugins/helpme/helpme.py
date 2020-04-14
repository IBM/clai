#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from collections import OrderedDict

from clai.tools.colorize_console import Colorize

from clai.server.plugins.helpme.data import Datastore
from clai.server.agent import Agent
from clai.server.command_message import State, Action, NOOP_COMMAND

from clai.server.logger import current_logger as logger


class HelpMeAgent(Agent):
    def __init__(self):
        super(HelpMeAgent, self).__init__()
        self.store = Datastore()

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

        logger.info("=========================== In Helpme Bot:post_execute ===================================")
        logger.info("State:\n Command: {}\n Error Code: {}\n Stderr: {}".format(state.command,
                                                                            state.result_code,
                                                                            state.stderr))
        logger.info("============================================================================")
        
        # DJF Start
        apis:OrderedDict=self.store.getAPIs()
        for api in apis:
            logger.info(f"DEBUG!!! ==>  {api}: {str(apis[api])}")
        # DJF End
        
        if state.result_code != '0':
            # Query data store to find closest matching forum
            forum = self.store.search(state.stderr, service='stack_exchange', size=1)

            if forum:
                logger.info("Success!!! Found relevant forums.")

                # Find closes match b/w relevant forum and manpages for unix
                manpages = self.store.search(forum[0]['Answer'], service='manpages', size=5)
                if manpages:
                    logger.info("Success!!! found relevant manpages.")

                    command = manpages['commands'][-1]
                    confidence = manpages['dists'][-1]

                    # FIXME: Artificially boosted confidence
                    confidence = 1.0

                    logger.info("Command: {} \t Confidence:{}".format(command, confidence))

                    return Action(suggested_command="man {}".format(command),
                                  description=Colorize().emoji(Colorize.EMOJI_ROBOT)
                                  .append(f"I did little bit of internet searching for you.\n")
                                  .info()
                                  .append("Post: {}\n".format(forum[0]['Content'][:384] + " ..."))
                                  .append("Answer: {}\n".format(forum[0]['Answer'][:256] + " ..."))
                                  .append("Link: {}\n\n".format(forum[0]['Url']))
                                  .warning()
                                  .append("Do you want to try: man {}".format(command))
                                  .to_console(),
                                  confidence=confidence
                                  )
                else:
                    logger.info("Failure: Manpage search")
                    logger.info("============================================================================")

                    return Action(suggested_command=NOOP_COMMAND,
                                  description=Colorize().emoji(Colorize.EMOJI_ROBOT)
                                  .append(
                                      f"Sorry. It looks like you have stumbled across a problem that even internet doesn't have answer to.\n")
                                  .info()
                                  .append(f"Have you tried turning it OFF and ON again. ;)")
                                  .to_console(),
                                  confidence=0.0
                                  )
            else:
                logger.info("Failure: Forum search")
                logger.info("============================================================================")
                return Action(suggested_command=NOOP_COMMAND,
                              description=Colorize().emoji(Colorize.EMOJI_ROBOT)
                              .append(
                                  f"Sorry. It looks like you have stumbled across a problem that even internet doesn't have answer to.\n")
                              .warning()
                              .append(f"Have you tried turning it OFF and ON again. ;)")
                              .to_console(),
                              confidence=0.0
                              )

        return Action(suggested_command=state.command)
