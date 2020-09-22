#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import spacy


class QuestionDetection(object):
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.WH_TAGS = [
            "WDT",
            "WP",
            "WP$",
            "WRB",
        ]  # WH word tags. These signify the presence of an interrogative word

    def is_question(self, text):
        """
        A function to check if text is phrased as a question.

        Algorithm:
            1. Test if the text ends with "?". If yes, then it's a question.
            2. Test if the text contains any "WH" word tags (indicative of WH type of question)

        Args:
            text (str): a text to be tested

        Returns:
            (bool): True if the text is a question.
        """

        if text.endswith("?"):
            return True

        doc = self.nlp(text)
        for token in doc:
            if token.tag_ in self.WH_TAGS:
                return True

        return False
