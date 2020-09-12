import tensorflow as tf
from tensorflow import keras
import numpy as np

print("TF Version: ", tf.__version__)
print("GPU is", "available" if tf.config.experimental.list_physical_devices("GPU") else "NOT AVAILABLE")

import numpy
import keras
print(numpy.__path__)
print(keras.__path__)

import sys
print("sys.path")
for p in sys.path:
    print(p)
