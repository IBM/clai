import html
import math

import numpy as np
import os, sys
import requests
import time
import scipy as sp

sys.path.append(os.path.join(
    os.path.dirname(__file__), "..", "tellina_learning_module"))

from bashlint import data_tools

WEBSITE_DEVELOP = False
CACHE_TRANSLATIONS = False

from website import functions
from website.cmd2html import tokens2html
#from website.models import NL, Command, NLRequest, URL, Translation, Vote, User
#from website.utils import get_tag, get_nl, get_command, NUM_TRANSLATIONS
#from website.utils import get_command

if not WEBSITE_DEVELOP:
    from website.backend_interface import translate_fun

def translate_clai(request_str):
    trans_list = []
    annotated_trans_list = []

    if not trans_list:
        if not WEBSITE_DEVELOP:
            # call learning model and store the translations
            batch_outputs, output_logits = translate_fun(request_str)
            # print('----------------------------------------------------------')
            # print(batch_outputs[0])
            # print('----------------------------------------------------------')
            # print(output_logits[0])
            # print('----------------------------------------------------------')

            if batch_outputs:
                top_k_predictions = batch_outputs[0]
                top_k_scores = output_logits[0]
                layers_top_k_scores = []

                # Storing all layer scores into an array
                for i in range(len(output_logits)):
                    layers_top_k_scores.append(output_logits[i])

                # for i in range(len(top_k_predictions)):
                #     pred_tree, pred_cmd = top_k_predictions[i]
                #     score = top_k_scores[i]
                #     cmd = get_command(pred_cmd)
                #     trans_set = Translation.objects.filter(nl=nl, pred_cmd=cmd)
                #     if not trans_set.exists():
                #         trans = Translation.objects.create(
                #             nl=nl, pred_cmd=cmd, score=score)
                #     else:
                #         for trans in trans_set:
                #             break
                #         trans.score = score
                #         trans.save()
                #     trans_list.append(trans)
                #     start_time = time.time()
                #     annotated_trans_list.append(tokens2html(pred_tree))
                #     print(time.time() - start_time)
                #     start_time = time.time()

    tellina_top_response_cmd = top_k_predictions[0][1]

    tellina_return = {
        'response': tellina_top_response_cmd,
        'confidence': '0.0'
    }
    return tellina_return

def main():
    print('----------------------------------------------------------')
    print(translate_clai("print top 10 largest files and directories"))

if __name__ == "__main__":
    main()
