import sys
import logging

from typing import Iterable
from typing import List

from dataclasses import dataclass

from nlpipes.callbacks.callbacks import Callback
from nlpipes.callbacks.callbacks import CallbackList
from nlpipes.data.data_types import InputFeatures


logger = logging.getLogger('__name__')

@dataclass
class Trainer():
    
    """ The trainer is written from scratch. It consists in 
    a custom training loop that trigger a set of `Callback`
    functions at given stages of the training procedure, 
    such as when:
     - the training/testing starts.
     - the training/testing ends.
     - a train/test epoch starts
     - a train/test epoch ends.
     - a train/test batch starts.
     - a train/test batch ends.
     ...
    """
    
    train_stream: Iterable[InputFeatures]
    test_stream: Iterable[InputFeatures]
    callbacks: List[Callback]
    num_epochs: int
    
    def train(self):
        
        callbacks = CallbackList(self.callbacks)
        
        try:
            callbacks.on_train_begin()
            
            for epoch in range(self.num_epochs):
                callbacks.on_epoch_begin(epoch)
                
                for step, batch in enumerate(self.train_stream):
                    callbacks.on_train_batch_begin(step, batch)
                    callbacks.on_train_batch_end(step, batch)
                    
                if self.test_stream:
                    callbacks.on_test_begin()
                    
                    for step, batch in enumerate(self.test_stream):
                        callbacks.on_test_batch_begin(step, batch)
                        callbacks.on_test_batch_end(step, batch)
                        
                    callbacks.on_test_end()
                    
                callbacks.on_epoch_end(epoch)
                
            callbacks.on_train_end()
             
        except:
            message = 'The training process has been stopped.'
            logger.info(message)
            