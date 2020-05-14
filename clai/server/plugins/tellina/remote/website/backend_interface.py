"""
Interface to the neural translation model.
"""
import tensorflow as tf

import os
import sys

learning_module_dir = os.path.join(os.path.dirname(__file__), "..",
                                   "tellina_learning_module")
sys.path.append(learning_module_dir)

#from website.utils import NUM_TRANSLATIONS
from encoder_decoder import data_utils
from encoder_decoder import decode_tools
from encoder_decoder import parse_args
from encoder_decoder import translate

CPU_ONLY=True
if CPU_ONLY:
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
else:
    os.environ["CUDA_VISIBLE_DEVICES"] = "2"

# initialize FLAGS by parsing a dummy argument list
if tf.__version__.startswith('2.0'):
    tf.compat.v1.app.flags.FLAGS(sys.argv[:1])
    FLAGS = tf.compat.v1.app.flags.FLAGS

FLAGS.demo = True
FLAGS.fill_argument_slots = False
FLAGS.num_nn_slot_filling = 5

FLAGS.encoder_topology = 'birnn'

FLAGS.sc_token_dim = 200
FLAGS.batch_size = 128
FLAGS.num_layers = 1
FLAGS.learning_rate = 0.0001
FLAGS.sc_input_keep = 0.6
FLAGS.sc_output_keep = 0.6
FLAGS.tg_input_keep = 0.6
FLAGS.tg_output_keep = 0.6

FLAGS.tg_token_use_attention = True
FLAGS.tg_token_attn_fun = 'non-linear'
FLAGS.attention_input_keep = 0.6
FLAGS.attention_output_keep = 0.6
FLAGS.beta = 0.0

FLAGS.token_decoding_algorithm = 'beam_search'
FLAGS.beam_size = 100
FLAGS.alpha = 1

FLAGS.min_vocab_frequency = 4
FLAGS.normalized = False
FLAGS.channel = 'partial.token'
FLAGS.use_copy = True
FLAGS.copy_fun = 'copynet'

FLAGS.dataset = 'bash'
FLAGS.data_dir = os.path.join(learning_module_dir, "data", FLAGS.dataset)
FLAGS.model_root_dir = os.path.join(learning_module_dir, "model", "seq2seq")

# Data-dependent parameters
FLAGS.max_sc_length = 42
FLAGS.max_tg_length = 57
FLAGS.sc_vocab_size = 1324
FLAGS.tg_vocab_size = 1219
FLAGS.max_sc_token_size = 100
FLAGS.max_tg_token_size = 100
buckets = [(13, 57), (18, 57), (42, 57)]

# Create tensorflow session
sess = tf.compat.v1.Session(config=tf.compat.v1.ConfigProto(allow_soft_placement=True,
    log_device_placement=FLAGS.log_device_placement))

# create model and load nerual model parameters.
model = translate.define_model(sess, forward_only=True, buckets=buckets)
print('loading models from {}'.format(FLAGS.model_dir))

vocabs = data_utils.load_vocabulary(FLAGS)

if FLAGS.fill_argument_slots:
    # Create slot filling classifier
    model_param_dir = os.path.join(FLAGS.model_dir, 'train.mappings.X.Y.npz')
    train_X, train_Y = data_utils.load_slot_filling_data(model_param_dir)
    slot_filling_classifier = classifiers.KNearestNeighborModel(
        FLAGS.num_nn_slot_filling, train_X, train_Y)
    print('Slot filling classifier parameters loaded.')
else:
    slot_filling_classifier = None

def translate_fun(sentence, slot_filling_classifier=slot_filling_classifier):
    print('translating |{}|'.format(sentence))
    list_of_translations = decode_tools.translate_fun(
        sentence, sess, model, vocabs, FLAGS, slot_filling_classifier)
    print('---------------------translation-------------------------------')
    return list_of_translations
