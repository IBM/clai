import pathlib
import sys
import os

submission_code_dirpath = pathlib.Path(__file__).parent.absolute()
tellina_modpath = os.path.join(submission_code_dirpath, 'tellina_learning_module')

os.environ['TELLINA_LEARNING_MODPATH'] = tellina_modpath

if str(submission_code_dirpath) not in sys.path:
    sys.path.insert(0, str(submission_code_dirpath))
if tellina_modpath not in sys.path:
    sys.path.insert(0, tellina_modpath)

from . import translate_cmd


def predict(invocations, result_cnt=5):
    """
    Function called by the evaluation script to interface the participants model
    `predict` function accepts the natural language invocations as input, and returns
    the predicted commands along with confidences as output. For each invocation,
    `result_cnt` number of predicted commands are expected to be returned.

    Args:
        1. invocations : `list (str)` : list of `n_batch` (default 16) natural language invocations
        2. result_cnt : `int` : number of predicted commands to return for each invocation

    Returns:
        1. commands : `list [ list (str) ]` : a list of list of strings of shape (n_batch, result_cnt)
        2. confidences: `list[ list (float) ]` : confidences corresponding to the predicted commands
                                                 confidence values should be between 0.0 and 1.0.
                                                 Shape: (n_batch, result_cnt)
    """

    n_batch = len(invocations)

    # `commands` and `confidences` have shape (n_batch, result_cnt)
    commands = [
        [''] * result_cnt
        for _ in range(n_batch)
    ]
    confidences = [
        [1.0] * result_cnt
        for _ in range(n_batch)
    ]

    ################################################################################################
    #     Participants should add their codes to fill predict `commands` and `confidences` here    #
    ################################################################################################

    for idx, inv in enumerate(invocations):

        # Call the translate method to retrieve translations and scores
        tellina_top_commands, tellina_top_scores, tellina_layers = translate_cmd.translate_clai(inv)

        # For testing evalAI docker push, just fill top command - just need to check
        # if tellina imports work correctly right now
        for i in range(result_cnt):
            commands[idx][i] = tellina_top_commands[i][1]

        # TODO: Not filling in confidences here, default value

    ################################################################################################
    #                               Participant code block ends                                    #
    ################################################################################################

    return commands, confidences
