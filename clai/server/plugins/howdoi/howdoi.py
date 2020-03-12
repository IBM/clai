#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

from clai.tools.colorize_console import Colorize

from clai.server.plugins.howdoi.data import Datastore
from clai.server.agent import Agent
from clai.server.command_message import State, Action, NOOP_COMMAND
from clai.server.plugins.howdoi.question_detection import QuestionDetection

from clai.server.logger import current_logger as logger


class HowDoIAgent(Agent):
    def __init__(self):
        super(HowDoIAgent, self).__init__()
        self.store = Datastore()
        self.questionIdentifier = QuestionDetection()

    def compute_simple_token_similarity(self, src_sequence, tgt_sequence):
        src_tokens = set([x.lower().strip() for x in src_sequence.split()])
        tgt_tokens = set([x.lower().strip() for x in tgt_sequence.split()])

        return len(src_tokens & tgt_tokens) / len(src_tokens)

    def get_next_action(self, state: State) -> Action:

        logger.info("================== In HowDoI Bot:get_next_action ========================")
        logger.info("User Command: {}".format(state.command))

        # Invoke "howdoi" plugin only when a question is asked
        is_question = self.questionIdentifier.is_question(state.command)

        if not is_question:
            return Action(
                suggested_command=state.command,
                confidence=0.0
            )

        # Query data store to find closest matching forum
        forum = self.store.search(state.command, service='stack_exchange', size=1)

        if forum:
            # Find closes match b/w relevant forum for unix
            logger.info("Success!!! Found relevant forums.")

            # Find closes match b/w relevant forum and manpages for unix
            manpages = self.store.search(forum[0]['Answer'], service='manpages', size=5)
            if manpages:
                logger.info("Success!!! found relevant manpages.")

                command = manpages['commands'][-1]
                confidence = manpages['dists'][-1]

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
