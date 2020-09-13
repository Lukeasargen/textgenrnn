from __future__ import absolute_import, division, print_function, unicode_literals

import numpy
import keras
import tensorflow as tf




print("Numpy Version: ", numpy.__version__)
print("Keras Version: ", keras.__version__)
print("TF Version: ", tf.__version__)
print("Eager mode: ", tf.executing_eagerly())
list_gpus = tf.config.experimental.list_physical_devices('GPU')
print("Num GPUs Available: ", len(list_gpus))
print("GPU is", "available" if list_gpus else "NOT AVAILABLE")
