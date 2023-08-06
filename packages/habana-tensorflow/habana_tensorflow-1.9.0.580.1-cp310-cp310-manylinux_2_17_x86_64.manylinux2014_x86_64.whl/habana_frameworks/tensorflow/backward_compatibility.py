###############################################################################
# Copyright (C) 2022 Habana Labs, Ltd. an Intel Company
# All Rights Reserved.
#
# Unauthorized copying of this file or any element(s) within it, via any medium
# is strictly prohibited.
# This file contains Habana Labs, Ltd. proprietary and confidential information
# and is subject to the confidentiality and license agreements under which it
# was provided.
#
###############################################################################

from packaging import version
import tensorflow as tf
from types import SimpleNamespace

# Additional layer for backward compatibility for
# API change between 2.11 and older versions of tf.
backward_compatible_optimizers = SimpleNamespace()

if version.parse(tf.keras.__version__) >= version.parse("2.11"):
    backward_compatible_optimizers.Adadelta = tf.keras.optimizers.legacy.Adadelta
    backward_compatible_optimizers.Adagrad = tf.keras.optimizers.legacy.Adagrad
    backward_compatible_optimizers.Adam = tf.keras.optimizers.legacy.Adam
    backward_compatible_optimizers.Adamax =  tf.keras.optimizers.legacy.Adamax
    backward_compatible_optimizers.Ftrl = tf.keras.optimizers.legacy.Ftrl
    backward_compatible_optimizers.Nadam = tf.keras.optimizers.legacy.Nadam
    backward_compatible_optimizers.Optimizer = tf.keras.optimizers.legacy.Optimizer
    backward_compatible_optimizers.RMSprop = tf.keras.optimizers.legacy.RMSprop
    backward_compatible_optimizers.SGD = tf.keras.optimizers.legacy.SGD
else:
    backward_compatible_optimizers.Adadelta = tf.keras.optimizers.Adadelta
    backward_compatible_optimizers.Adagrad = tf.keras.optimizers.Adagrad
    backward_compatible_optimizers.Adam = tf.keras.optimizers.Adam
    backward_compatible_optimizers.Adamax =  tf.keras.optimizers.Adamax
    backward_compatible_optimizers.Ftrl = tf.keras.optimizers.Ftrl
    backward_compatible_optimizers.Nadam = tf.keras.optimizers.Nadam
    backward_compatible_optimizers.Optimizer = tf.keras.optimizers.Optimizer
    backward_compatible_optimizers.RMSprop = tf.keras.optimizers.RMSprop
    backward_compatible_optimizers.SGD = tf.keras.optimizers.SGD
