import argparse
import time
import os
import json
from datetime import datetime

from submission_code import main as predictor
from utils.metric_utils import compute_metric
from utils.dataset import Nlc2CmdDS
from utils.dataloaders import Nlc2CmdDL


def get_parser():
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--annotation_filepath', type=str, required=True)
    parser.add_argument('--params_filepath', type=str, required=True)
    parser.add_argument('--output_folderpath', type=str, required=True)

    return parser


def get_dataloader(annotation_filepath):
    nlc2cmd_ds = Nlc2CmdDS(annotation_filepath)
    nlc2cmd_dl = Nlc2CmdDL(nlc2cmd_ds, batchsize=8, shuffle=True)
    return iter(nlc2cmd_dl)


def get_params(params_filepath):
    with open(params_filepath, 'r') as f:
        params = json.load(f)
    return params


def validate_predictions(predicted_cmds, predicted_confds, n_batch, result_cnt):

    assert len(predicted_cmds) == n_batch, \
        f'{len(predicted_cmds)} commands predicted for {n_batch} invocations'

    assert len(predicted_confds) == n_batch, \
        f'{len(predicted_confds)} confidences predicted for {n_batch} invocations'

    for i in range(n_batch):
        assert 1 <= len(predicted_cmds[i]) <= result_cnt, \
            f'{len(predicted_cmds[i])} commands predicted for an invocations. Expected between 1 and {result_cnt}'

        assert 1 <= len(predicted_confds[i]) <= result_cnt, \
            f'{len(predicted_confds[i])} confidences predicted for an invocations. Expected between 1 and {result_cnt}'

        assert not (False in [0.0 <= x <= 1.0 for x in predicted_confds[i]]), \
            f'Confidence value beyond the allowed range of [0.0, 1.0] found in predictions'


def get_predictions(nlc2cmd_dl):

    result_cnt = 5
    i = 0
    ground_truths = []
    predicted_cmds, predicted_confds = [], []
    
    for invocations, cmds in nlc2cmd_dl:
        batch_predicted_cmds, batch_predicted_confd = predictor.predict(invocations, result_cnt=result_cnt)
        validate_predictions(batch_predicted_cmds, batch_predicted_confd, len(invocations), result_cnt)

        ground_truths.extend(cmds)
        predicted_cmds.extend(batch_predicted_cmds)
        predicted_confds.extend(batch_predicted_confd)

        if i % 15 == 0:
            now = datetime.now().strftime('%d/%m %H:%M:%S')
            print(f'\t{now} :: {i} batches predicted')
        i += 1

    return ground_truths, predicted_cmds, predicted_confds


def compute_score(ground_truths, predicted_cmds, predicted_confds, metric_params):

    score = float("-inf")

    for grnd_truth_cmd in ground_truths:
        for i, predicted_cmd in enumerate(predicted_cmds):
            predicted_confidence = predicted_confds[i]
            pair_score = compute_metric(predicted_cmd, predicted_confidence, grnd_truth_cmd, metric_params)
            score = max(score, pair_score)

    print('-' * 50)
    print(f'Ground truth: {ground_truths}')
    print(f'Predictions: {predicted_cmds}')
    print(f'Score: {score}')

    return score


def evaluate_model(annotation_filepath, params_filepath):

    try:
        params = get_params(params_filepath)

        nlc2cmd_dl = get_dataloader(annotation_filepath)

        stime = time.time()
        fn_return = get_predictions(nlc2cmd_dl)
        total_time_taken = time.time() - stime

        ground_truths, predicted_cmds, predicted_confds = fn_return
        n = len(ground_truths)

        print('----------------------- Predictions -----------------------')

        scores = [
            compute_score(ground_truths[i], predicted_cmds[i], predicted_confds[i], params)
            for i in range(n)
        ]

        print(f'sum: {sum(scores)}, n: {n}')
        print('----------------------- Predictions -----------------------')

        mean_score = sum(scores) / float(n)
        time_taken = total_time_taken / float(n)

        result = {
            'status': 'success',
            'time_taken': time_taken,
            'score': mean_score
        }

    except Exception as err:
        result = {
            'status': 'error',
            'error_message': str(err)
        }

    return result


if __name__ == '__main__':
    
    parser = get_parser()
    args = parser.parse_args()

    os.makedirs(args.output_folderpath, exist_ok=True)

    result = evaluate_model(args.annotation_filepath, args.params_filepath)

    with open(os.path.join(args.output_folderpath, 'result.json'), 'w') as f:
        json.dump(result, f)
