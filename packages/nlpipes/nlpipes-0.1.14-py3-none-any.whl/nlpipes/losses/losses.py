from typing import Union

import tensorflow as tf


def softmax_cross_entropy(
    labels: tf.Tensor,
    logits: tf.Tensor,
) -> tf.Tensor:
    """ Computes the softmax cross-entropy single label classification """
    softmax = tf.nn.softmax_cross_entropy_with_logits
    return softmax(labels, logits, axis=-1, name='Loss')


def sigmoid_cross_entropy(
    labels: tf.Tensor,
    logits: tf.Tensor,
) -> tf.Tensor:
    """ Computes the sigmoid cross-entropy for multi label classification """
    sigmoid = tf.nn.sigmoid_cross_entropy_with_logits
    return sigmoid(labels, logits, name='Loss')    
    