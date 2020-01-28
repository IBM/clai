#
# Copyright (C) 2020 IBM. All Rights Reserved.
#
# See LICENSE.txt file in the root directory
# of this source tree for licensing information.
#

import spacy


class QuestionDetection(object):

    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        self.WH_TAGS = ['WDT', 'WP', 'WP$', 'WRB']  # WH word tags. These signify the presence of an interrogative word

    def is_question(self, text):

        if text.endswith('?'):
            return True

        doc = self.nlp(text)
        for token in doc:
            if token.tag_ in self.WH_TAGS:
                return True

        return False
