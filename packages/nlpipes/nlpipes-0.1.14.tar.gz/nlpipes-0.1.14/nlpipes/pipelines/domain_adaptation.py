import os
import logging

from typing import List
from typing import Optional
from typing import Union

from pathlib import Path

from dataclasses import dataclass

import tensorflow as tf
import transformers

from transformers import (
    PretrainedConfig,
    PreTrainedTokenizer,
    TFPreTrainedModel,
)

from nlpipes.trainers.trainers import Trainer

from nlpipes.losses.losses import softmax_cross_entropy

from nlpipes.data.data_loaders import DataLoader
from nlpipes.data.data_processors import LanguageModelingDataProcessor

from nlpipes.data.data_selectors import DataSelector
from nlpipes.data.data_augmentors import VocabAugmentor
from nlpipes.data.data_cleaners import clean

from nlpipes.data.data_utils import (
     create_examples,
     split_examples,
)

from nlpipes.data.data_types import (
     Document,
     Corpus,
     Token,
     InputExample,
)

from nlpipes.callbacks.callbacks import (
     Callback,
     TrainingStep,
     History,
     ModelCheckpoint,
     CSVLogger,
     ProgbarLogger,
     EarlyStopping,
     TimedStopping,
)

transformers.logging.set_verbosity_error()

logger = logging.getLogger('__name__')

#uncomment row below for debugging rust tokenizer
#os.environ["RUST_BACKTRACE"]="full" 


@dataclass
class TFPipelineForMaskedLM():
    """ The `pipeline` for the masked language modeling task.
    There are almost no abstractions. Just three standard
    classes are required to use the pipeline: configuration,
    model and tokenizer. 
    
    Args
    ----------
    model(TFPreTrainedModel):
       The model used for the classification task`.
       It usually composed of a bert layer with a
       classification head on top.
    
    tokenizer(PreTrainedTokenizerFast):
       The rust tokenizer used to convert the input
       text into encoded vectors.
    
    config(PretrainedConfig): 
       The model configuration file.
    """
    
    model: TFPreTrainedModel
    tokenizer: PreTrainedTokenizer
    config: PretrainedConfig
    
    def train(
        self,
        texts: Corpus,
        train_frac: float=0.75,
        test_frac: float=0.25,
        num_epochs: int=2,
        batch_size: int=4,
        lr: float=2e-5,
        min_delta: float = 0.01,
        patience: int = 5,
        time_limit: int = 86400,
        rand_seed: int = 69,
        target_corpus_size: Union[int, float]=0.5,
        target_vocab_size: int=31000,
        similarity_metrics: Optional[List[str]]=['euclidean'],
        diversity_metrics: Optional[List[str]]=['entropy'],
        keep_checkpoints: bool = False,
        save_corpus_dir: str = './sub_corpus',
        checkpoints_dir: str = './checkpoints',
        logs_dir: str = './logs',
    ) -> TFPreTrainedModel:
        """ Train the model on a masked modeling task:
        80% [MASK], 10% random words and 10% same word. """
        
        data_selector = DataSelector(
            name='DataSelection',
            tokenizer=self.tokenizer,
            target_corpus_size=target_corpus_size,
            similarity_metrics=similarity_metrics,
            diversity_metrics=diversity_metrics,
        )
        
        vocab_augmentor = VocabAugmentor(
            name='VocabAugmentation',
            tokenizer=self.tokenizer,
            target_vocab_size=target_vocab_size,
            cased=False,
        )

        clean_texts = [clean(text) for text in texts]
        selected_texts = data_selector(clean_texts)
        new_tokens = vocab_augmentor.get_new_tokens(selected_texts)
        
        self.tokenizer.add_tokens(new_tokens)
        self.model.resize_token_embeddings(len(self.tokenizer))
        os.makedirs(save_corpus_dir, exist_ok=True) 
        corpus_path = os.path.join(save_corpus_dir, 'selected_corpus.txt')         
        Path(corpus_path).write_text('\n'.join(selected_texts))
        
        examples = create_examples(
            texts=selected_texts, 
            labels=None,
            config=self.config,
        )
        
        train_examples, test_examples = split_examples(
            examples=examples,
            train_frac=train_frac,
            test_frac=test_frac, 
            shufffle=True, 
        )

        data_processor = LanguageModelingDataProcessor(
            name='DataProcessingForLM',
            tokenizer=self.tokenizer,
            config=self.config,
            mlm_proba=0.15
        )
        
        train_stream = DataLoader(
            name='TrainDataLoading',
            examples=train_examples,
            batch_size=batch_size,
            data_processor=data_processor,
        )
        
        test_stream = DataLoader(
            name='TestDataLoading',
            examples=test_examples,
            batch_size=batch_size,
            data_processor=data_processor,
        )
        
        training_step = TrainingStep(
            name='BatchTraining',
            model=self.model,
            loss_function=softmax_cross_entropy,
            optimizer=tf.optimizers.Adam(lr),
        )
        
        history = History(
            name='History', 
            training_step=training_step,
            loss_metric = tf.metrics.Mean,
            acc_metric = tf.metrics.CategoricalAccuracy,
        )
        
        model_checkpoint = ModelCheckpoint(
            name='ModelCheckpointing',
            model=self.model, 
            history=history,
            checkpoints_dir=checkpoints_dir,
        )
        
        early_stopping = EarlyStopping(
            name='EarlyStopping', 
            history=history,
            direction='minimize',
            min_delta=min_delta,
            patience=patience,
        )
        
        timed_stopping = TimedStopping(
            name='TimedStopping',
            time_limit=time_limit,
        )
        
        csv_logger = CSVLogger(
            name='CSVLogging',
            logs_dir=logs_dir,
        )
        
        progbar_logger = ProgbarLogger(
            name='ProgbarLogging',
            batch_size=batch_size,
            num_epochs=num_epochs,
            history=history,
            num_samples=sum([
                train_stream.num_examples(),
                test_stream.num_examples(),
            ])
        )
        
        callbacks = [
            training_step,
            history,
            model_checkpoint,
            csv_logger,
            progbar_logger,
            early_stopping,
            timed_stopping,
        ]
        
        trainer = Trainer(
            train_stream=train_stream,
            test_stream=test_stream,
            callbacks=callbacks,
            num_epochs=num_epochs,
        )
        
        trainer.train()
        
        if keep_checkpoints == False:
            shutil.rmtree(checkpoints_dir)
        
        return history
    
    def evaluate(self):
        """ Evaluate the model performance on new data
        according to the user-defined evaluation metric """
        raise NotImplementedError
        
    def predict(self):
        """ Get predictions a new unseen data """
        raise NotImplementedError
    
    def save(self, save_dir: str):
        """ Save the model and the tokenizer on disk """
        
        os.makedirs(save_dir, exist_ok=True)        
        self.model.save_pretrained(save_dir)
        self.tokenizer.save_pretrained(save_dir)
        self.config.save_pretrained(save_dir)
        