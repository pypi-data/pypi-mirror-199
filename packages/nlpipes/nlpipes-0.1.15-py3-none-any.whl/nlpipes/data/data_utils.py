from typing import Any
from typing import Callable
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

from itertools import chain

import numpy as np
import tensorflow as tf

from transformers import PretrainedConfig

from sklearn.preprocessing import MultiLabelBinarizer

from nlpipes.data.data_types import InputExample


def chunk() -> Callable[[str], List[str]]:
    """  Chunk text into shorter sequences. """  
    
    def chunk_into_sentences(texts: str) -> List[str]:
        """ Chunk text with regular-expressions """
        on_regex = '(?<=[^A-Z].[.?]) +(?=[A-Z])'
        sequences = [re.split(on_regex, text) for text in texts]
        sequences = [sequence for sublist in sequences for sequence in sublist]
        return sequences
    
    def chunk_into_whatever(texts: str) -> List[str]:
        raise NotImplementedError
    
    chunk_fn = chunk_into_sentences

    return chunk_fn
    
    
def create_examples(
    texts: List[str],
    labels: Optional[List[str]],
    config: PretrainedConfig,
   ) -> List[InputExample]:
    """ Serialize each input raw data into examples. """
    
    if labels:
        label2id = config.label2id
        
        if get_labels_depth(labels)==1:
            labels = [
                label2id[label] for label in labels
            ]
        elif get_labels_depth(labels)==2:
            labels = [
                [label2id[label] for label in sub_label]
                for sub_label in labels
            ]
            
        examples = [
            InputExample(text, label=label)
            for text, label in zip(texts, labels)
        ]
        
    else:
        examples = [InputExample(text) for text in texts]
        
    return examples


def split_examples(
    examples: List[InputExample],
    train_frac: float = None,
    test_frac: float = None, 
    shufffle: bool = True,
    random_seed: int = 42,
   ) -> Tuple[InputExample]:
    """ split the input example into a training and a
    testing set. """
    
    n_examples = len(examples)
    n_train = int(np.ceil(n_examples*train_frac))
    n_test = int(np.ceil(n_examples*test_frac))
    n_total = n_train + n_test
    
    if shufffle:
        random_state = np.random.RandomState(random_seed)
        order = random_state.permutation(n_examples)
        train_idx = order[:n_train]
        test_idx = order[n_train:n_total]
    else:
        train_idx = np.arange(n_train)
        test_idx = np.arange(n_train, n_total)
    
    train_examples = [examples[idx] for idx in train_idx]
    test_examples = [examples[idx] for idx in test_idx]
    
    return train_examples, test_examples


def generate_batches(
    X: List[str], 
    Y: List[str], 
    batch_size: int,
) -> Iterable[List[Any]]:
    """ Yield a batch of examples from the input raw data """
    
    X_batch = list()
    Y_batch = list()
    
    for x, y in zip(X,Y):
        X_batch.append(x)
        Y_batch.append(y)
        if len(X_batch) < batch_size:
            continue
        yield X_batch, Y_batch    
        X_batch = list()
        Y_batch = list()


def get_labels_depth(labels: List[Any]) -> int:
    """ Get the depth level of a potentially nested list of labels """
    level = 1
    if isinstance(labels, list):
        return level + max(get_labels_depth(label) for label in labels)
    else:
        return 0


def convert_onehot_to_ids(one_hot):
    mask = tf.dtypes.cast(one_hot, tf.bool)
    s = tf.shape(mask)
    r = tf.reshape(
            tf.range(s[-1]),
            tf.concat([
                tf.ones(
                    tf.rank(one_hot) - 1, 
                    tf.int32),
                [-1]
            ],
            axis=0)
    )
    r = tf.tile(r, tf.concat([s[:-1], [1]], axis=0))
    ragged_tensor = tf.ragged.boolean_mask(r, mask)
    
    return ragged_tensor.to_list()

def convert_ids_to_onehot(ids, depth, dtype):
    one_hot_tensor = tf.convert_to_tensor(
        MultiLabelBinarizer(
            classes=range(depth)
        ).fit_transform(ids),
        dtype=dtype
    )
    
    return one_hot_tensor
