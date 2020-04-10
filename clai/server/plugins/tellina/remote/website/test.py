import tensorflow as tf
import sys
import os
learning_module_dir = os.path.join("", "..",
                                   "tellina_learning_module")
sys.path.append(learning_module_dir)
#tf.app.flags.FLAGS(sys.argv[:1])
#FLAGS = tf.app.flags.FLAGS
print(tf.__version__)
#print(FLAGS)