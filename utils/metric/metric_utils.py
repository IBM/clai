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


def pad_arrays(array1, array2):
    n_arr1 = len(array1)
    n_arr2 = len(array2)

    if n_arr1 > n_arr2:
        array2 = array2 + [None] * (n_arr1 - n_arr2)
    elif n_arr2 > n_arr1:
        array1 = array1 + [None] * (n_arr2 - n_arr1)

    return array1, array2


def get_flag_score(ground_truth_utility, predicted_utility):

    ground_truth_flags = get_utility_flags(ground_truth_utility)
    predicted_flags = get_utility_flags(predicted_utility)

    if len(ground_truth_flags) == 0 and len(predicted_flags) == 0:
        # return a score of 1.0 when there are no flags to predict
        return 1.0

    ground_truth_flagnames = set([node.value for node in ground_truth_flags])
    predicted_flagnames = set([node.value for node in predicted_flags])

    intersection_len = len(ground_truth_flagnames.intersection(predicted_flagnames))
    union_len = len(ground_truth_flagnames.union(predicted_flagnames))
    Z = max(1, len(predicted_flagnames), len(ground_truth_flagnames))

    score = (2 * intersection_len - union_len) / float(Z)

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

    ground_truth_utilities, predicted_utilities = pad_arrays(ground_truth_utilities, predicted_utilities)

    score = []
    u1 = 1.0
    u2 = 1.0

    for ground_truth_utility, predicted_utility in zip(ground_truth_utilities, predicted_utilities):
        utility_score = get_utility_score(ground_truth_utility, predicted_utility)
        flag_score = get_flag_score(ground_truth_utility, predicted_utility)

        flag_score_normed = (u1 + u2 * flag_score) / (u1 + u2)
        prediction_score = predicted_confidence * (
            (utility_score * flag_score_normed) -
            (1 - utility_score)
        )
        score.append(prediction_score)

    score_mean = 0.0 if len(score) == 0 else np.mean(score)
    return score_mean
