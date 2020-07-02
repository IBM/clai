"""
Compute keyword overlap between two commands.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import collections
import numpy as np

from bashlint import data_tools, nast
from bashlint.data_tools import bash_parser


def get_utilities(ast):
    def extract_utility_nodes(node):
        try:
            if node.is_utility():
                utilities[node.value] = utilities.get(node.value, 0) + 1
        except AttributeError:
            return
        else:
            for child in node.children:
                extract_utility_nodes(child)

    utilities = {}
    extract_utility_nodes(ast)
    return utilities


def get_utility_nodes(ast):
    def extract_utility_nodes(node):
        try:
            if node.is_utility():
                utilities.append(node)
        except AttributeError:
            return
        else:
            for child in node.children:
                extract_utility_nodes(child)

    utilities = []
    extract_utility_nodes(ast)
    return utilities


def get_utility_flags(utility_node):
    def extract_flags(node):
        try:
            if node.is_option():
                options.append(node)
        except AttributeError:
            return
        else:
            for child in node.children:
                extract_flags(child)

    options = []
    extract_flags(utility_node)
    return options


def get_content_tokens(ast):
    content_tokens = collections.defaultdict(int)
    for compound_token in data_tools.ast2tokens(ast, loose_constraints=True,
            arg_type_only=True, with_prefix=True, with_flag_argtype=True):
        kind_token = compound_token.split(nast.KIND_PREFIX)
        if len(kind_token) == 2:
            kind, token = kind_token
        else:
            kind = ''
            token = kind_token[0]
        if kind.lower() != 'argument':
            content_tokens[token] += 1
    return content_tokens


def utility_match_score(ast1, ast2):
    utilities_dict1 = get_utilities(ast1)
    utilities_dict2 = get_utilities(ast2)
    num_overlap = 0.0

    for utility in utilities_dict1.items():
        if utility in utilities_dict2:
            num_overlap += utilities_dict1[utility] * utilities_dict2[utility]

    norm1 = sum([x**2 for x in utilities_dict1.values()])
    norm2 = sum([x**2 for x in utilities_dict2.values()])

    if norm1 == 0 or norm2 == 0:
        return 0
    return num_overlap / (norm1 * norm2)


def get_utility_score(ground_truth_utility, predicted_utility):
    def get_node_value(node):
        if isinstance(node, nast.Node):
            return node.value.lower()
        return None

    ground_truth_utility_name = get_node_value(ground_truth_utility)
    predicted_utility_name = get_node_value(predicted_utility)
    score = float(ground_truth_utility_name == predicted_utility_name)
    return score


def get_flag_score(ground_truth_utility, predicted_utility):

    ground_truth_flags = get_utility_flags(ground_truth_utility)
    predicted_flags = get_utility_flags(predicted_utility)

    if len(ground_truth_flags) == 0 and len(predicted_flags) == 0:
        # return a score of 1.0 when there are no flags to predict
        return 1.0

    ground_truth_flagnames = [node.value for node in ground_truth_flags]
    predicted_flagnames = [node.value for node in predicted_flags]

    correctly_predicted_flags = [flag in ground_truth_flagnames for flag in predicted_flagnames]

    num_correctly_predicted = sum(correctly_predicted_flags)
    num_incorrectly_predicted = len(predicted_flagnames) - num_correctly_predicted
    Z = len(predicted_flagnames)
    Z = 1 if Z == 0 else Z

    score = (num_correctly_predicted - num_incorrectly_predicted) / float(Z)
    return score


def compute_metric(predicted_cmd, predicted_confidence, ground_truth_cmd):

    if type(predicted_cmd) is not str:
        predicted_cmd = str(predicted_cmd)
    if type(ground_truth_cmd) is not str:
        ground_truth_cmd = str(ground_truth_cmd)
    if type(predicted_confidence) is not float:
        try:
            predicted_confidence = float(predicted_confidence)
        except Exception:
            predicted_confidence = 1.0

    predicted_ast = bash_parser(predicted_cmd)
    ground_truth_ast = bash_parser(ground_truth_cmd)

    predicted_utilities = get_utility_nodes(predicted_ast)
    ground_truth_utilities = get_utility_nodes(ground_truth_ast)

    score = []
    u1 = 1.0
    u2 = 1.0

    for i, ground_truth_utility in enumerate(ground_truth_utilities):
        predicted_utility = predicted_utilities[i] if i < len(predicted_utilities) else None

        utility_score = get_utility_score(ground_truth_utility, predicted_utility)
        flag_score = get_flag_score(ground_truth_utility, predicted_utility)

        flag_score_normed = (u1 + u2 * flag_score) / (u1 + u2)
        prediction_score = predicted_confidence * utility_score * flag_score_normed
        score.append(prediction_score)

    score_mean = 0.0 if len(score) == 0 else np.mean(score)
    return score_mean
