from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import sys

if sys.version_info > (3, 0):
    from six.moves import xrange

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import numpy as np

import datetime, time
import re
import shutil

from bashlint import bash, data_tools
from encoder_decoder import data_utils, slot_filling
from eval import tree_dist
from nlp_tools import constants, format_args, tokenizer

APOLOGY_MSG = "Sorry, I don't know how to translate this command."


def demo(sess, model, FLAGS):
    """
    Simple command line decoding interface.
    """
    # Decode from standard input.
    sys.stdout.write('> ')
    sys.stdout.flush()
    sentence = sys.stdin.readline()

    vocabs = data_utils.load_vocabulary(FLAGS)

    while sentence:
        if FLAGS.fill_argument_slots:
            slot_filling_classifier = get_slot_filling_classifer(FLAGS)
            batch_outputs, sequence_logits = translate_fun(sentence, sess, model,
                vocabs, FLAGS, slot_filling_classifier=slot_filling_classifier)
        else:
            batch_outputs, sequence_logits = translate_fun(sentence, sess, model,
                vocabs, FLAGS)
        if FLAGS.token_decoding_algorithm == 'greedy':
            tree, pred_cmd, outputs = batch_outputs[0]
            score = sequence_logits[0]
            print('{} ({})'.format(pred_cmd, score))
        elif FLAGS.token_decoding_algorithm == 'beam_search':
            if batch_outputs:
                top_k_predictions = batch_outputs[0]
                top_k_scores = sequence_logits[0]
                for j in xrange(min(FLAGS.beam_size, 10, len(batch_outputs[0]))):
                    if len(top_k_predictions) <= j:
                        break
                    top_k_pred_tree, top_k_pred_cmd = top_k_predictions[j]
                    print('Prediction {}: {} ({}) '.format(
                        j+1, top_k_pred_cmd, top_k_scores[j]))
                print()
            else:
                print(APOLOGY_MSG)
        print('> ', end='')
        sys.stdout.flush()
        sentence = sys.stdin.readline()


def translate_fun(data_point, sess, model, vocabs, FLAGS,
                  slot_filling_classifier=None):
    tg_ids = [data_utils.ROOT_ID]
    decoder_features = [[tg_ids]]
    if type(data_point) is str:
        source_str = data_point
        encoder_features = query_to_encoder_features(data_point, vocabs, FLAGS)
    else:
        source_str = data_point[0].sc_txt
        encoder_features = [[data_point[0].sc_ids]]
        if FLAGS.use_copy and FLAGS.copy_fun == 'copynet':
            encoder_features.append([data_point[0].csc_ids])

    if FLAGS.use_copy and FLAGS.copy_fun == 'copynet':
        # append dummy copynet target features (
        # used only for computing training objectives)
        ctg_ids = [data_utils.ROOT_ID]
        decoder_features.append([ctg_ids])
        # tokenize the source string with minimal changes on the token form
        copy_tokens = [query_to_copy_tokens(source_str, FLAGS)]
    else:
        copy_tokens = None
    if FLAGS.normalized:
        _, entities = tokenizer.ner_tokenizer(source_str)
        sc_fillers = [entities[0]]
    else:
        sc_fillers = None

    # Which bucket does it belong to?
    bucket_ids = [b for b in xrange(len(model.buckets))
                  if model.buckets[b][0] > len(encoder_features[0][0])]
    bucket_id = min(bucket_ids) if bucket_ids else (len(model.buckets) - 1)
    
    # Get a 1-element batch to feed the sentence to the model.
    formatted_example = model.format_batch(
        encoder_features, decoder_features, bucket_id=bucket_id)

    # Compute neural network decoding output
    model_outputs = model.step(sess, formatted_example, bucket_id,
                               forward_only=True)
    sequence_logits = model_outputs.sequence_logits

    decoded_outputs = decode(model_outputs, FLAGS, vocabs, sc_fillers=sc_fillers,
                             slot_filling_classifier=slot_filling_classifier,
                             copy_tokens=copy_tokens)
    print(decoded_outputs)
    return decoded_outputs, sequence_logits


def decode(model_outputs, FLAGS, vocabs, sc_fillers=None,
           slot_filling_classifier=None, copy_tokens=None):
    """
    Transform the neural network output into readable strings and apply output
    filtering (if any).
    :param encoder_inputs:
    :param model_outputs:
    :param FLAGS:
    :param vocabs:
    :param sc_fillers:
    :param slot_filling_classifier:
    :return batch_outputs: nested list of (target_ast, target) tuples
        - target_ast is a python tree object for target languages that we know
          how to parse and a dummy string for those we don't
        - target is the output string
    """
    rev_tg_vocab = vocabs.rev_tg_vocab

    encoder_outputs = model_outputs.encoder_hidden_states
    decoder_outputs = model_outputs.decoder_hidden_states

    if FLAGS.fill_argument_slots:
        assert(sc_fillers is not None)
        assert(slot_filling_classifier is not None)
        assert(encoder_outputs is not None)
        assert(decoder_outputs is not None)

    output_symbols = model_outputs.output_symbols
    batch_size = len(output_symbols)
    batch_outputs = []
    num_output_examples = 0

    for batch_id in xrange(batch_size):
        def as_str(output, r_tg_vocab):
            if output < FLAGS.tg_vocab_size:
                token = r_tg_vocab[output]
            else:
                if FLAGS.use_copy and FLAGS.copy_fun == 'copynet':
                    source_id = output - FLAGS.tg_vocab_size
                    if source_id >= 0 and source_id < len(copy_tokens[batch_id]):
                        token = copy_tokens[batch_id][source_id]
                    else:
                        return data_utils._UNK
                else:
                    return data_utils._UNK
            return token

        top_k_predictions = output_symbols[batch_id]
        if FLAGS.token_decoding_algorithm == 'beam_search':
            assert(len(top_k_predictions) == FLAGS.beam_size)
            beam_outputs = []
        else:
            # pack greedy decoding results into size-1 beam
            top_k_predictions = [top_k_predictions]

        for beam_id in xrange(len(top_k_predictions)):
            # Step 1: transform the neural network output into readable strings
            prediction = top_k_predictions[beam_id]
            outputs = [int(pred) for pred in prediction]
            
            # If there is an EOS symbol in outputs, cut them at that point.
            if data_utils.EOS_ID in outputs:
                outputs = outputs[:outputs.index(data_utils.EOS_ID)]
            if data_utils.PAD_ID in outputs:
                outputs = outputs[:outputs.index(data_utils.PAD_ID)]
            output_tokens = []
            tg_slots = {}
            for token_id in xrange(len(outputs)):
                output = outputs[token_id]
                pred_token = as_str(output, rev_tg_vocab)
                if data_tools.flag_suffix in pred_token:
                    pred_token = pred_token.split(data_tools.flag_suffix)[0]
                # process argument slots
                if pred_token in bash.argument_types:
                    if token_id > 0 and format_args.is_min_flag(
                        rev_tg_vocab[outputs[token_id-1]]):
                        pred_token_type = 'Timespan'
                    else:
                        pred_token_type = pred_token
                    tg_slots[token_id] = (pred_token, pred_token_type)
                output_tokens.append(pred_token)

            if FLAGS.channel == 'partial.token':
                # process partial-token outputs
                merged_output_tokens = []
                buffer = ''
                load_buffer = False
                for token in output_tokens:
                    if load_buffer:
                        if token == data_utils._ARG_END:
                            merged_output_tokens.append(buffer)
                            load_buffer = False
                            buffer = ''
                        else:
                            buffer += token
                    else:
                        if token == data_utils._ARG_START:
                            load_buffer = True
                        else:
                            merged_output_tokens.append(token)
                if buffer:
                    merged_output_tokens.append(buffer)
                output_tokens = merged_output_tokens
    
            if FLAGS.channel == 'char':
                target = ''
                for char in output_tokens:
                    if char == data_utils.constants._SPACE:
                        target += ' '
                    else:
                        target += char
            else:
                target = ' '.join(output_tokens)
            
            # Step 2: checvik if the predicted command template is grammatical
            if FLAGS.grammatical_only and not FLAGS.explain:
                if FLAGS.dataset.startswith('bash'):
                    target = re.sub('( ;\s+)|( ;$)', ' \\; ', target)
                    target_ast = data_tools.bash_parser(target, verbose=False)
                elif FLAGS.dataset.startswith('regex'):
                    # TODO: check if a predicted regular expression is legal
                    target_ast = '__DUMMY_TREE__'
                else:
                    target_ast = data_tools.paren_parser(target)
                # filter out non-grammatical output
                if target_ast is None:
                    continue
            else:
                target_ast = '__DUMMY_TREE__'

            # Step 3: check if the predicted command templates have enough
            # slots to hold the fillers (to rule out templates that are
            # trivially unqualified)
            output_example = False
            if FLAGS.explain or not FLAGS.dataset.startswith('bash') \
                    or not FLAGS.normalized:
                output_example = True
            else:
                # Step 3: match the fillers to the argument slots
                batch_sc_fillers = sc_fillers[batch_id]
                if len(tg_slots) >= len(batch_sc_fillers):
                    if FLAGS.fill_argument_slots:
                        target_ast, target, _ = slot_filling.stable_slot_filling(
                            output_tokens, batch_sc_fillers, tg_slots, None,
                            encoder_outputs[batch_id],
                            decoder_outputs[batch_id*FLAGS.beam_size+beam_id],
                            slot_filling_classifier, verbose=False)
                    else:
                        output_example = True
                    if not output_example and (target_ast is not None):
                        output_example = True

            if output_example:
                if FLAGS.token_decoding_algorithm == 'greedy':
                    batch_outputs.append((target_ast, target))
                else:
                    beam_outputs.append((target_ast, target))
                num_output_examples += 1

            # The threshold is used to increase decoding speed
            if num_output_examples == 20:
                break

        if FLAGS.token_decoding_algorithm == 'beam_search':
            if beam_outputs:
                batch_outputs.append(beam_outputs)

    return batch_outputs


def decode_set(sess, model, dataset, top_k, FLAGS, verbose=False):
    """
    Compute top-k predictions on the dev/test dataset and write the predictions
    to disk.

    :param sess: A TensorFlow session.
    :param model: Prediction model object.
    :param top_k: Number of top predictions to compute.
    :param FLAGS: Training/testing hyperparameter settings.
    :param verbose: If set, also print decoding results to screen.
    """
    nl2bash = FLAGS.dataset.startswith('bash') and not FLAGS.explain

    tokenizer_selector = 'cm' if FLAGS.explain else 'nl'
    grouped_dataset = data_utils.group_parallel_data(
        dataset, tokenizer_selector=tokenizer_selector)
    vocabs = data_utils.load_vocabulary(FLAGS)
    rev_sc_vocab = vocabs.rev_sc_vocab

    ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d-%H%M%S')
    pred_file_path = os.path.join(model.model_dir, 'predictions.{}.{}'.format(
        model.decode_sig, ts))
    pred_file = open(pred_file_path, 'w')
    eval_file_path = os.path.join(model.model_dir, 'predictions.{}.{}.csv'.format(
        model.decode_sig, ts))
    eval_file = open(eval_file_path, 'w')
    eval_file.write('example_id, description, ground_truth, prediction, ' +
                    'correct template, correct command\n')
    for example_id in xrange(len(grouped_dataset)):
        key, data_group = grouped_dataset[example_id]

        sc_txt = data_group[0].sc_txt.strip()
        sc_tokens = [rev_sc_vocab[i] for i in data_group[0].sc_ids]
        if FLAGS.channel == 'char':
            sc_temp = ''.join(sc_tokens)
            sc_temp = sc_temp.replace(constants._SPACE, ' ')
        else:
            sc_temp = ' '.join(sc_tokens)
        tg_txts = [dp.tg_txt for dp in data_group]
        tg_asts = [data_tools.bash_parser(tg_txt) for tg_txt in tg_txts]
        if verbose:
            print('\nExample {}:'.format(example_id))
            print('Original Source: {}'.format(sc_txt.encode('utf-8')))
            print('Source: {}'.format(sc_temp.encode('utf-8')))
            for j in xrange(len(data_group)):
                print('GT Target {}: {}'.format(j+1, data_group[j].tg_txt.encode('utf-8')))

        if FLAGS.fill_argument_slots:
            slot_filling_classifier = get_slot_filling_classifer(FLAGS)
            batch_outputs, sequence_logits = translate_fun(data_group, sess, model,
                vocabs, FLAGS, slot_filling_classifier=slot_filling_classifier)
        else:
            batch_outputs, sequence_logits = translate_fun(data_group, sess, model,
                vocabs, FLAGS)
        if FLAGS.tg_char:
            batch_outputs, batch_char_outputs = batch_outputs

        eval_row = '{},"{}",'.format(example_id, sc_txt.replace('"', '""'))
        if batch_outputs:
            if FLAGS.token_decoding_algorithm == 'greedy':
                tree, pred_cmd = batch_outputs[0]
                if nl2bash:
                    pred_cmd = data_tools.ast2command(
                        tree, loose_constraints=True)
                score = sequence_logits[0]
                if verbose:
                    print('Prediction: {} ({})'.format(pred_cmd, score))
                pred_file.write('{}\n'.format(pred_cmd))
            elif FLAGS.token_decoding_algorithm == 'beam_search':
                top_k_predictions = batch_outputs[0]
                if FLAGS.tg_char:
                    top_k_char_predictions = batch_char_outputs[0]
                top_k_scores = sequence_logits[0]
                num_preds = min(FLAGS.beam_size, top_k, len(top_k_predictions))
                for j in xrange(num_preds):
                    if j > 0:
                        eval_row = ',,'
                    if j < len(tg_txts):
                        eval_row += '"{}",'.format(tg_txts[j].strip().replace('"', '""'))
                    else:
                        eval_row += ','
                    top_k_pred_tree, top_k_pred_cmd = top_k_predictions[j]
                    if nl2bash:
                        pred_cmd = data_tools.ast2command(
                            top_k_pred_tree, loose_constraints=True)
                    else:
                        pred_cmd = top_k_pred_cmd
                    pred_file.write('{}|||'.format(pred_cmd.encode('utf-8')))
                    eval_row += '"{}",'.format(pred_cmd.replace('"', '""'))
                    temp_match = tree_dist.one_match(
                        tg_asts, top_k_pred_tree, ignore_arg_value=True)
                    str_match = tree_dist.one_match(
                        tg_asts, top_k_pred_tree, ignore_arg_value=False)
                    if temp_match:
                        eval_row += 'y,'
                    if str_match:
                        eval_row += 'y'
                    eval_file.write('{}\n'.format(eval_row.encode('utf-8')))
                    if verbose:
                        print('Prediction {}: {} ({})'.format(
                            j+1, pred_cmd.encode('utf-8'), top_k_scores[j]))
                        if FLAGS.tg_char:
                            print('Character-based prediction {}: {}'.format(
                                j+1, top_k_char_predictions[j].encode('utf-8')))
                pred_file.write('\n')
        else:
            print(APOLOGY_MSG)
            pred_file.write('\n')
            eval_file.write('{}\n'.format(eval_row))
            eval_file.write('\n')
            eval_file.write('\n')
    pred_file.close()
    eval_file.close()
    shutil.copyfile(pred_file_path, os.path.join(FLAGS.model_dir,
        'predictions.{}.latest'.format(model.decode_sig)))
    shutil.copyfile(eval_file_path, os.path.join(FLAGS.model_dir,
        'predictions.{}.latest.csv'.format(model.decode_sig)))


def get_slot_filling_classifer(FLAGS):
    # create slot filling classifier
    mapping_param_dir = os.path.join(FLAGS.model_dir, 'train.mappings.X.Y.npz')
    npz = np.load(mapping_param_dir)
    train_X = npz['arr_0']
    train_Y = npz['arr_1']
    slot_filling_classifier = slot_filling.KNearestNeighborModel(FLAGS.num_nn_slot_filling, train_X, train_Y)
    print('Slot filling classifier parameters loaded.')
    return slot_filling_classifier


# --- Compute query features
def query_to_encoder_features(sentence, vocabs, FLAGS):
    """
    Convert a natural language query into feature vectors used by the encoder.
    """
    if FLAGS.channel == 'char':
        tokens = data_utils.nl_to_characters(sentence)
        init_vocab = data_utils.CHAR_INIT_VOCAB
    elif FLAGS.channel == 'partial.token':
        tokens = data_utils.nl_to_partial_tokens(sentence, tokenizer.basic_tokenizer)
        init_vocab = data_utils.TOKEN_INIT_VOCAB
    else:
        if FLAGS.normalized:
            tokens = data_utils.nl_to_tokens(sentence, tokenizer.ner_tokenizer)
        else:
            tokens = data_utils.nl_to_tokens(sentence, tokenizer.basic_tokenizer)
        init_vocab = data_utils.TOKEN_INIT_VOCAB
    sc_ids = data_utils.tokens_to_ids(tokens, vocabs.sc_vocab)
    encoder_features = [[sc_ids]]
    if FLAGS.use_copy and FLAGS.copy_fun == 'copynet':
        csc_ids = []
        for i, t in enumerate(tokens):
            if not t in init_vocab and t in vocabs.tg_vocab:
                csc_ids.append(vocabs.tg_vocab[t])
            else:
                csc_ids.append(len(vocabs.tg_vocab) + i)
        encoder_features.append([csc_ids])
    return encoder_features


def query_to_copy_tokens(sentence, FLAGS):
    if FLAGS.channel == 'char':
        tokens = data_utils.nl_to_characters(sentence)
    elif FLAGS.channel == 'partial.token':
        tokens = data_utils.nl_to_partial_tokens(
            sentence, tokenizer.basic_tokenizer, to_lower_case=False,
            lemmatization=False)
    else:
        tokens = data_utils.nl_to_tokens(
            sentence, tokenizer.basic_tokenizer, to_lower_case=False,
            lemmatization=False)
    return tokens

# --- Visualization --- #
def visualize_attn_alignments(M, source, target, rev_sc_vocab,
                              rev_tg_vocab, output_path):
    target_length, source_length = M.shape

    nl = [rev_sc_vocab[x] for x in source]
    cm = []
    for i, x in enumerate(target):
        cm.append(rev_tg_vocab[x])
        if rev_tg_vocab[x] == data_utils._EOS:
            break

    plt.clf()
    if len(target) == 0:
        i = 0
    plt.imshow(M[:i+1, :], interpolation='nearest', cmap=plt.cm.Blues)

    pad_size = source_length - len(nl)
    plt.xticks(xrange(source_length),
               [x.replace('$$', '') for x in reversed(
                   nl + [data_utils._PAD] * pad_size)],
               rotation='vertical')
    plt.yticks(xrange(len(cm)), [x.replace('$$', '') for x in cm],
               rotation='horizontal')

    plt.colorbar()

    plt.savefig(output_path, bbox_inches='tight')
