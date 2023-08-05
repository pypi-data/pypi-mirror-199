import os
import sys
import logging
import time
import datetime

from abc import ABC, abstractmethod
from collections import defaultdict

from dataclasses import astuple
from dataclasses import dataclass
from dataclasses import field

import numpy as np
import tensorflow as tf
from transformers import TFPreTrainedModel

from tqdm.auto import tqdm

from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Tuple,
)

from nlpipes.data.data_types import (
    InputFeatures,
    TFSequenceClassifierBatchOutput,
)

logger = logging.getLogger('__name__')


"""
`Callbacks` encapsulate a set of functions to be applied at given
stages of the training procedure to customize the trainer behavior. 
The relevant callbacks functions will then be called at the 
various stages of the model training lifecycle, such as when:
 - the training starts.
 - the training ends.
 - the testing starts.
 - the testing ends.
 - an epoch starts
 - an epoch ends.
 - a batch starts.
 - a batch ends.
"""

class Callback(ABC):
    
    """ Abstract base class for callback objects. """
    
    def on_train_begin(self):
        """ Called at the beginning of the training. """
        
    def on_train_end(self):
        """ Called at the end of the training. """
        
    def on_test_begin(self):
        """ Called at the beginning of the evaluation. """
        
    def on_test_end(self):
        """ Called at the end of the evaluation. """
    
    def on_epoch_begin(self, *args):
        """ Called at the beginning of an epoch. """
        
    def on_epoch_end(self, *args):
        """ Called at the end of an epoch. """
    
    def on_train_batch_begin(self, *args):
        """ Called at the beginning of a training batch. """
    
    def on_train_batch_end(self, *args):
        """ Called at the end of a training batch. """
    
    def on_test_batch_begin(self, *args):
        """ Called at the beginning of a test batch. """

    def on_test_batch_end(self, *args):
        """ Called at the end of a testing batch. """


@dataclass
class CallbackList(Callback):
    """ Internal class that just calls the list of callbacks.
    The CallbackList serves two main purposes:
        1. It stores all the callbacks.
        2. It allows to call all of the individual callbacks 
           easily. For example, if we have three callbacks 
           that do something at the end of an epoch, then 
           callbacks.on_epoch_end() will call the three
           callback objects in order. 
    """

    callbacks: List[Callback]
    
    def on_train_begin(self, *args):
        for callback in self.callbacks:
            callback.on_train_begin(*args)
        
    def on_train_end(self, *args):
        for callback in self.callbacks:
            callback.on_train_end(*args)
        
    def on_test_begin(self, *args):
        for callback in self.callbacks:
            callback.on_test_begin(*args)
        
    def on_test_end(self, *args):
        for callback in self.callbacks:
            callback.on_test_end(*args)

    def on_epoch_begin(self, *args):
        for callback in self.callbacks:
            callback.on_epoch_begin(*args)

    def on_epoch_end(self, *args):
        for callback in self.callbacks:
            callback.on_epoch_end(*args)
            
    def on_train_batch_begin(self, *args):
        for callback in self.callbacks:
            callback.on_train_batch_begin(*args)

    def on_train_batch_end(self, *args):
        for callback in self.callbacks:
            callback.on_train_batch_end(*args)

    def on_test_batch_begin(self, *args):
        for callback in self.callbacks:
            callback.on_test_batch_begin(*args)

    def on_test_batch_end(self, *args):
        for callback in self.callbacks:
            callback.on_test_batch_end(*args) 


@dataclass
class TrainingStep(Callback):
    """ Callback that define the training step. The training step is
    a single iteration of the training process. It consists of a 
    forward pass (where the obj:`model` makes predictions based on
    the input data) and a backward pass (where the obj:`optimizer`
    updates the obj:`model` weights and biases based on the difference
    between the predicted output and the expected output as expressed
    by the obj:`loss_function`).
    """
    
    name: str = 'TrainingStep'
    model: TFPreTrainedModel = None
    optimizer: tf.optimizers.Optimizer = None
    loss_function: tf.losses = None
    
    def train_step(self, input_batch: InputFeatures):
        """ Train the obj:`model` on a single batch of examples. """
        
        with tf.GradientTape() as tape:
            output_batch = self.model.call(
                input_ids=input_batch.input_ids,
                attention_mask=input_batch.attention_mask,
                token_type_ids=input_batch.token_type_ids,
                training=True,
            )
            
            loss = self.loss_function(
                input_batch.label, output_batch.logits
            )
            
        variables = self.model.trainable_variables
        gradients = tape.gradient(loss, variables)
        
        self.optimizer.apply_gradients(
            zip(gradients, variables)
        )
        
        return TFSequenceClassifierBatchOutput(
            loss=loss,
            logits=output_batch.logits,
            hidden_states=output_batch.hidden_states,
            attentions=output_batch.attentions,
        )
    
    def test_step(self, input_batch: InputFeatures):
        """ Test the obj:`model` on a single batch of examples. """
        
        output_batch = self.model.call(
                  input_ids=input_batch.input_ids,
                  attention_mask=input_batch.attention_mask,
                  token_type_ids=input_batch.token_type_ids,
                  training=False,
        )
        
        loss = self.loss_function(
            input_batch.label, output_batch.logits
        )
        
        return TFSequenceClassifierBatchOutput(
            loss=loss,
            logits=output_batch.logits,
            hidden_states=output_batch.hidden_states,
            attentions=output_batch.attentions,
        )
    
    def on_train_begin(self):
        message = self.model.summary()
        print(message)
        
    def on_train_batch_begin(self, step: int, batch: InputFeatures):
        self.train_step_output = self.train_step(batch)
             
    def on_test_batch_begin(self, step: int, batch: InputFeatures):
        self.test_step_output = self.test_step(batch)

        
@dataclass
class History(Callback):
    """ Callback that record the performance of the model 
    during training. It stores all the evaluation metrics 
    such as loss and accuracy at each training and testing
    steps. This allows to track the progress of the model
    over time, and can be used by other callbacks, e.g. to
    detect when the model has reached its optimal performance.
    """
    
    name: str = 'History'
    epoch: int = field(default_factory=int)
    loss_metric: Callable[[], tf.metrics.Metric] = None
    acc_metric: Callable[[], tf.metrics.Metric] = None
    training_step: Callback = None
    logs: Dict = field(default_factory=lambda: defaultdict(dict))
    
    def __post_init__(self):
        """ """
        self.loss_train_metric = self.loss_metric()
        self.loss_test_metric = self.loss_metric()
        self.acc_train_metric = self.acc_metric
        self.acc_test_metric = self.acc_metric
        
    def on_train_begin(self):
        """ Initialize the logger with the performance metrics
        that need to be historized """
        self.logs['loss'] = {}
        self.logs['acc'] = {}
        self.logs['val_loss'] = {}
        self.logs['val_acc'] = {}
    
    def on_epoch_begin(self, epoch: int):
        """ Resets all of the metric state variables """
        self.epoch = epoch
        self.loss_train_metric.reset_states()
        self.loss_test_metric.reset_states()
        self.acc_train_metric.reset_states()
        self.acc_test_metric.reset_states()
        
    def on_epoch_end(self, epoch: int):
        """ Display the performance metrics after each epoch """
        message = f"\nEpoch - {epoch+1}  \n" \
                  f"---------- \n" \
                  f"Train - " \
                  f"loss: {self.logs['loss'][epoch]:1.4f} - " \
                  f"accuracy: {self.logs['acc'][epoch]:1.4f} \n" \
                  f"Test - " \
                  f"loss: {self.logs['val_loss'][epoch]:1.4f} - " \
                  f"accuracy: {self.logs['val_acc'][epoch]:1.4f} \n"        
        
        logger.info(message)

    def on_train_batch_end(self, step: int, input_batch: InputFeatures):
        """ Compute the performance metrics after each batch at 
        training time """
        epoch = self.epoch
        output_batch = self.training_step.train_step_output

        labels = input_batch.label
        logits = output_batch.logits
        loss = output_batch.loss
        
        self.loss_train_metric.update_state(loss)
        self.acc_train_metric.update_state(labels, logits)
        self.logs['loss'][epoch] = self.loss_train_metric.result()
        self.logs['acc'][epoch] = self.acc_train_metric.result()
        
        
    def on_test_batch_end(self, step: int, input_batch: InputFeatures):
        """ Compute the performance metrics after each batch at 
        testing time """
        
        epoch = self.epoch
        output_batch = self.training_step.test_step_output
        
        labels = input_batch.label
        logits = output_batch.logits
        loss = output_batch.loss
        
        self.loss_test_metric.update_state(loss)
        self.acc_test_metric.update_state(labels, logits)
        
        self.logs['val_loss'][epoch] = self.loss_test_metric.result()
        self.logs['val_acc'][epoch] = self.acc_test_metric.result()
        
    @property
    def best_result(self) -> float:
        """ Return the best performance metric among epochs """
        return min(self.logs['val_loss'].values())
    

@dataclass
class ModelCheckpoint(Callback):
    """ Callback that save the model weights and configuration 
    after each epoch and to keep track of the best model """
    
    name: str = 'ModelCheckpointing'
    model: TFPreTrainedModel = None
    history: History = None
    direction: str = 'minimize'
    best_result: float = np.inf
    best_model_dir: str = ''
    checkpoints_dir: str = 'checkpoints'

    def __post_init__(self):
        """ Create the directory for saving checkpoints """
        if self.direction not in ['minimize', 'maximize']:
            raise ValueError
        if self.direction == 'maximize':
            self.best_result = 0

        if not os.path.isdir(self.checkpoints_dir):
            abs_path = os.path.abspath(self.checkpoints_dir)
            text = f'Make a checkpoint directory: {abs_path}'
            logger.info(text)
            os.makedirs(self.checkpoints_dir)

    def on_epoch_end(self, epoch: int):
        """ Save the model checkpoint if the performance improves """
        result = self.history.logs['val_loss'][epoch]
        diff = self.best_result - result
        is_better = diff > 0 if self.direction == 'minimize' else diff < 0
        if is_better:
            name = f'epoch-{epoch:02d}-{result:.2f}'
            model_dir = os.path.join(self.checkpoints_dir, name)
            os.mkdir(model_dir)
            self.model.config.architectures = self.model.__class__.__name__
            self.model.save_pretrained(model_dir)
            self.best_result = result
            self.best_model_dir = model_dir


@dataclass
class CSVLogger(Callback):
    """ Callback that store the logs of the performance metrics
    into a csv file. """
    
    name: str = 'CSVLogger'
    logs_dir: str = None
    level: int = 20
    msg_format: str = '%(asctime)s [%(levelname)-5s] %(message)s'

    def __post_init__(self):
        root_logger = logging.getLogger('__name__')
        root_logger.setLevel(self.level)
        root_logger.propagate = False
        formatter = logging.Formatter(self.msg_format, 
                                      datefmt='%Y-%m-%d %H:%M:%S')
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        
        root_logger.addHandler(console)
        if self.logs_dir:
            logs_dir = os.path.abspath(self.logs_dir)
            os.makedirs(logs_dir, exist_ok=True)
            file_path = os.path.join(logs_dir, 'experiment.log')
            file_handler = logging.FileHandler(file_path, mode='w')
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)


@dataclass
class EarlyStopping(Callback):
    """ Callback that stop training the model once a certain metric
    is no longer improving. The metric used is typically the 
    validation loss, but it can also be a metric such as accuracy
    or precision """
    
    name: str = 'EarlyStopping'
    history: History = None
    patience: int = 3
    min_delta: float = 0.01
    best_result: float = np.inf
    current_patience: int = 0
    direction: str = 'maximize'

    def __post_init__(self):
        if self.direction not in ['minimize', 'maximize']:
            raise ValueError
        if self.direction == 'maximize':
            self.best_result = 0

    def on_epoch_end(self, epoch: int):
        """ Check if the model is improving after each epoch
        and stop the training process if no improvement after
        a certain amount of iteration."""
        result = self.history.logs['val_loss'][epoch]
        diff = self.best_result - result
        is_better = diff > self.min_delta if self.direction == 'minimize' \
            else diff < self.min_delta * -1
        if is_better:
            self.best_result = result
            self.current_patience = 0
            return
        self.current_patience += 1
        if self.current_patience >= self.patience:
            raise Exception('Early stopping of the training')


@dataclass
class TimedStopping(Callback):
    """ Callbacks that stop training the model when a 
    specified amount of time has passed.
    
    Args:
        time_limit: maximum amount of time in seconds 
             before stopping.
        stopped_epoch: the epoch number where the training
              stopped.
    """

    name: str = 'TimedStopping'
    time_limit: int = 86000
    stopped_epoch: int = None

    def get_config(self):
        config = {"seconds": self.time_limit}
        base_config = super().get_config()
        return {**base_config, **config}
    
    def on_train_begin(self):
        self.stopping_time = time.time() + self.time_limit
        
    def on_epoch_end(self, epoch: int):
        if time.time() >= self.stopping_time:
            self.stopped_epoch = epoch
            formatted_time = datetime.timedelta(seconds=self.time_limit)
            message = "Timed stopping at epoch {} after training for {}".format(
                self.stopped_epoch + 1, formatted_time
            )
            raise Exception(message)

    def on_train_end(self):
        if self.stopped_epoch is not None:
            formatted_time = datetime.timedelta(seconds=self.time_limit)
            message = "Timed stopping at epoch {} after training for {}".format(
                self.stopped_epoch + 1, formatted_time
            )
            logger.info(message)


@dataclass
class ProgbarLogger(Callback):
    """ Callbacks that display a progress bar with performance metrics
    to monitor the progress of a model's training in the console """ 
    
    name: str = 'ProgbarLogger'
    history: History = None
    metric: Callable = tf.metrics.Mean
    epoch: int = field(default_factory=int)
    num_samples: int = None
    num_epochs: int = None
    batch_size: int = None
    show_overall_progress: bool = False
    show_epoch_progress: bool = True
    update_per_second: int = 10
    is_training = False

    def __post_init__(self):
        self.tqdm = tqdm
        self.num_steps: int = int(self.num_samples/self.batch_size)
        self.update_interval = 1/self.update_per_second
        self.last_update_time = time.time()
        self.bar_format: str = "Batch {n_fmt}/{total_fmt}{bar} " \
                               "ETA: {remaining}s - {desc}"
        self.metrics_format: str = "{name}: {value:0.4f}" 
        self.metrics_separator: str = " - "
        
    def _initialize_progbar(self, hook, epoch):
        self.num_samples_seen = 0
        self.steps_to_update = 0
        self.steps_so_far = 0
        self.train_logs = defaultdict(float)
        self.test_logs = defaultdict(float)
        
        if hook == "train":
            current_epoch_description = "Epoch {epoch}/{num_epochs}".format(
                epoch=epoch+1, num_epochs=self.num_epochs
            )
            if self.show_epoch_progress:
                print(current_epoch_description)
                self.epoch_progress_tqdm=self.tqdm(
                    total=self.num_steps,
                    position=0,
                    bar_format=self.bar_format,
                    leave=False,
                    dynamic_ncols=True,
                    unit="steps",
                )
        elif hook == "test":
            if self.show_epoch_progress:
                self.epoch_progress_tqdm=self.tqdm(
                    desc="Testing progress",
                    total=self.num_steps,
                    position=0,
                    bar_format=self.bar_format,
                    leave=False,
                    dynamic_ncols=True,
                    unit="steps",
                )

    def _update_progbar(self):
        self.num_samples_seen += self.batch_size
        self.steps_to_update += 1
        self.steps_so_far += 1

        if self.steps_so_far <= self.num_steps:  
            now = time.time()
            time_diff = now - self.last_update_time
            if self.show_epoch_progress and time_diff >= self.update_interval:
                
                self.epoch_progress_tqdm.desc = \
                     f"loss: {self.train_logs['loss']:.4f} - " \
                     f"accuracy: {self.train_logs['acc']:.4f} - " \
                     f"val_loss: {self.test_logs['loss']:.4f} - " \
                     f"val_accuracy: {self.test_logs['acc']:.4f}"

                self.epoch_progress_tqdm.update(self.steps_to_update)
                self.steps_to_update = 0
                self.last_update_time = now
                
    def _clean_up_progbar(self, hook):
        if self.show_epoch_progress:
            self.epoch_progress_tqdm.miniters = 0
            self.epoch_progress_tqdm.mininterval = 0
            self.epoch_progress_tqdm.update(
               self.num_steps - self.epoch_progress_tqdm.n
           )
            self.epoch_progress_tqdm.close()
                 
    def on_train_begin(self):
        self.is_training = True
        
    def on_train_end(self):
        self.is_training = False
        self._clean_up_progbar("train")
        
    def on_test_begin(self):
        if not self.is_training:
            self._initialize_progbar("test", epoch=None)
            
    def on_test_end(self):
        if not self.is_training:
            self._clean_up_progbar("test")
            
    def on_epoch_begin(self, epoch: int):
        self.epoch = epoch
        self._initialize_progbar("train", epoch)
    
    def on_epoch_end(self, epoch: int):
        self._clean_up_progbar("train")
        if self.show_overall_progress:
            self.overall_progress_tqdm.update(1)
        self.epoch_progress_tqdm.close()

    def on_train_batch_end(self, step: int, input_batch: InputFeatures):
        logs = defaultdict(float)
        logs["loss"] = self.history.logs['loss'][self.epoch]
        logs["acc"] = self.history.logs['acc'][self.epoch]
        self.train_logs = logs
        self._update_progbar()
        
    def on_test_batch_end(self, step: int, input_batch: InputFeatures):
        logs = defaultdict(float)
        logs["loss"] = self.history.logs['val_loss'][self.epoch]
        logs["acc"] = self.history.logs['val_acc'][self.epoch]
        self.test_logs = logs 
        self._update_progbar()
