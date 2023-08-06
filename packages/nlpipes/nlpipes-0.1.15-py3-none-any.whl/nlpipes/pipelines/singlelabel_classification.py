import os
import logging
import shutil

from typing import List
from typing import Optional

from dataclasses import dataclass

from pathlib import Path

import tensorflow as tf
import transformers

from transformers import (
    PretrainedConfig,
    PreTrainedTokenizerFast,
    TFPreTrainedModel,
    TFAutoModelForMaskedLM,
    AutoConfig,
    AutoTokenizer,
)

from tokenizers.pre_tokenizers import Whitespace

from nlpipes.trainers.trainers import Trainer
from nlpipes.losses.losses import softmax_cross_entropy

from nlpipes.data.data_loaders import DataLoader
from nlpipes.data.data_selectors import DataSelector
from nlpipes.data.data_augmentors import VocabAugmentor
from nlpipes.data.data_processors import SingleLabelDataProcessor
from nlpipes.data.data_cleaners import clean

from nlpipes.data.data_utils import (
     create_examples,
     split_examples,
     generate_batches,
     chunk,
)

from nlpipes.data.data_types import (
     Corpus,
     Document,
     Token,
     InputExample,
     InputExamples,
     InputTokens,
     InputFeatures,
     Predictions,
     Outcomes,
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

# uncomment row below for debugging rust tokenizer
# os.environ["RUST_BACKTRACE"]="full" 


@dataclass
class TFPipelineForSingleLabelClassification():
    """ The pipeline for single-label sequence 
    classification. There are almost no abstractions. 
    Just three standard classes are required to use 
    pipeline: configuration, model and tokenizer.
    
    Args
    ----------
    model(TFPreTrainedModel):
       The model used for the classification task`.
       It is simply a bert layer with a classification
       head on top.
    
    tokenizer(PreTrainedTokenizerFast):
       The rust tokenizer used to convert the input
       text into encoded vectors.
    
    config(PretrainedConfig): 
       The model configuration file.
    """
    
    model: TFPreTrainedModel
    tokenizer: PreTrainedTokenizerFast
    config: PretrainedConfig
    
    def train(self, 
              X: List[str], 
              Y: List[str],
              train_frac: float = 0.75,
              test_frac: float = 0.25,
              num_epochs: int = 3,
              batch_size: int = 16,
              seq_max_len: int = 512,
              learning_rate: float = 2e-5,
              beta_1: float = 0.9,
              beta_2: float = 0.999,
              patience: int = 2,
              min_delta: float = 0.01,
              time_limit: int = 86400,
              random_seed: int = 42,
              keep_checkpoints: bool = False,
              checkpoints_dir: str = './checkpoints',
              logs_dir: str = './logs',
             ) -> List[History]:
        """ Train a model for single-label classification.
        Most of the training process is implemented through 
        callbacks functions. Even the actual training step 
        (calculating the gradient and updating the weights 
        using an optimizer) is implemented as callbacks and
        is not part of the Trainer itself. This provide a 
        modular architecture that allows new ideas to be 
        implemented without having to change and increase
        the complexity of the trainer. """
        
        examples = create_examples(
            texts=X, 
            labels=Y,
            config=self.config,
        )
        
        train_examples, test_examples = split_examples(
            examples,
            train_frac=train_frac,
            test_frac=test_frac,
            shufffle=True,
            random_seed=random_seed,
        )          
        
        data_processor = SingleLabelDataProcessor(
            name='DataProcessing',
            tokenizer=self.tokenizer,
            config=self.config,
            seq_max_len=seq_max_len,
        )
        
        train_stream = DataLoader(
            name='TrainDataLoader',
            examples=train_examples,
            batch_size=batch_size,
            data_processor=data_processor,
            seed=random_seed,
        )
        
        test_stream = DataLoader(
            name='TestDataLoader',
            examples=test_examples,
            batch_size=batch_size,
            data_processor=data_processor,
            seed=random_seed,
        )
        
        training_step = TrainingStep(
            name='TrainingStep',
            model=self.model,
            loss_function=softmax_cross_entropy,
            optimizer=tf.optimizers.experimental.AdamW(
                learning_rate=learning_rate,
                beta_1=beta_1,
                beta_2=beta_2,
            ),
        )
        
        history = History(
            name='History', 
            training_step=training_step,
            loss_metric=tf.metrics.Mean,
            acc_metric=tf.metrics.CategoricalAccuracy(),
        )
        
        model_checkpoint = ModelCheckpoint(
            name='ModelCheckpoint',
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
            name='ProgbarLogger',
            batch_size=batch_size,
            num_epochs=num_epochs,
            history=history,
            num_samples=sum([
                train_stream.num_examples(),
                test_stream.num_examples(),
            ]))
        
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
    
    def evaluate(self,
                 X: List[str],
                 Y: List[str],
                 metric: tf.metrics.Metric,
                 batch_size: int = 32,
                ) -> tf.metrics.Metric:
        """ Evaluate the model performance on new data
        according to the user-defined evaluation metric """
        
        for texts, labels in generate_batches(X, Y, batch_size):
            examples = self.preprocess(texts, labels)
            features = self.transform(examples)
            predictions = self.classify(features)
            
            y_true = examples.labels
            y_pred = predictions.labels
            
            metric.update_state(y_true, y_pred)
        
        return metric.result()
    
    def predict(self, 
                texts: Corpus, 
                chunk_text: bool = False,
               ) -> Outcomes:
        """ Get predictions on new unlabeled data """
         
        examples = self.preprocess(texts)
        features = self.transform(examples)
        predictions = self.classify(features)
        completions = self.postprocess(predictions)
        
        return completions
    
    def preprocess(self,
                   texts: Corpus,
                   labels: Optional[str] = None,
                   chunk_text: Optional[bool] = False,
                  ) -> InputExamples:
        """ Serialize each raw text into examples. 
        Raw texts can eventually be chunk into spans """
        
        if labels:
            label2id = self.config.label2id
            labels_id = [label2id[label] for label in labels]
            examples = InputExamples(texts, labels=labels_id)
        else:
            texts = chunk(text) if chunk_text else texts
            examples = InputExamples(texts)
        
        return examples
    
    def transform(self, examples: InputExamples) -> InputFeatures: 
        """ Transform human-readable sequences into encoded
        features that can be use as input by the model. """

        inputs = self.tokenizer(
           examples.texts,
           add_special_tokens=True,
           padding=True,
           truncation=True,
           max_length=160,
           is_split_into_words = False,
           return_attention_mask=True,
           return_token_type_ids=True,
           return_tensors='tf',
        )

        features = InputFeatures(
           input_ids=inputs['input_ids'],
           attention_mask=inputs['attention_mask'],
           token_type_ids=inputs['token_type_ids'],
        )

        return features

    def classify(self, features: InputFeatures) -> Predictions:
        """ Predict the label index matching the maximum 
        prediction score and compute the loss value associated
        with each prediction. """

        outputs = self.model.call(
            input_ids=features.input_ids,
            attention_mask=features.attention_mask,
            token_type_ids=features.token_type_ids,
        )

        logits = outputs.logits
        scores = tf.nn.softmax(logits, axis=1)
        labels = tf.argmax(logits, axis=-1)
        labels_onehot = tf.one_hot(labels, self.config.num_labels)
        losses = softmax_cross_entropy(labels_onehot, logits)
        
        predictions = Predictions(
            labels=labels,
            scores=scores,
            losses=losses,
        )
        
        return predictions

    def postprocess(self, predictions: Predictions) -> Outcomes:
        """ Post-process the predictions. We convert tensors 
        into more convenient python lists and also convert the 
        predicted labels ids into their original name. """
          
        labels = predictions.labels.numpy()
        scores = predictions.scores.numpy()
        losses = predictions.losses.numpy()

        labels = labels.tolist()
        scores = scores.tolist()
        losses = losses.tolist()
        
        id2label = self.config.id2label
        labels = [id2label[label] for label in labels]
        
        outcomes = Outcomes(
            labels=labels,
            scores=scores,
            losses=losses,
        )

        return outcomes
    
    def save(self, save_dir: str):
        """ Save the trained model on disk """
        
        os.makedirs(save_dir, exist_ok=True)
        self.model.save_pretrained(save_dir)
        self.tokenizer.save_pretrained(save_dir)
        self.config.save_pretrained(save_dir)
