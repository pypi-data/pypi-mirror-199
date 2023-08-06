<!-- PROJECT NAME -->
<div align="center">
   <img src="https://raw.githubusercontent.com/uyanik/Images/b90c13ff8e580b2ecb2468889ed5ab1d52633d2e/logo.png" alt="nlpipes_logo" title="nlpipes logo">
  <h2>Text Classification with Transformers</h2>
</div>

<div align="center">
    <a href="https://opensource.org/licenses/Apache-2.0">
       <img alt="Licence" src="https://img.shields.io/badge/License-Apache_2.0-blue.svg">
    </a>
     <a href="https://pypi.org/project/nlpipes/">
       <img alt="PyPi Version" src="https://img.shields.io/pypi/pyversions/nlpipes">
    </a> 
    <a href="https://pypi.org/project/nlpipes/">
        <img alt="PyPi Package Version" src="https://img.shields.io/pypi/v/nlpipes">
    </a>
    <!--
    <a href="https://pepy.tech/project/nlpipes/">
        <img alt="PyPi Downloads" src="https://static.pepy.tech/badge/nlpipes/month">
    </a>
    -->
</div>

<div align="center">
    <a href=""><strong>Documentation</strong></a>
    • <a href=""><strong>References</strong></a>
</div>


<div align="center">
  <img src="https://ik.imagekit.io/m0ci8dgk4/nlpipes_screenshot_w_309qBjx.png?ik-sdk-version=javascript-1.4.3&updatedAt=1678033602383" alt="nlpipes_screenshot" title="nlpipes screenshot">
</div>


## Overview
`NLPipes` provides an easy way to use Transformers-based models for training, evaluation and inference on a diversity of text classification tasks, including:

* **Single-label classification**: Assign one label to each text. A typical use case is sentiment detection where one want to detect the overall sentiment polarity (e.g., positive, neutral, negative) in a review.
* **Multi-labels classification**: Assign one or more label to each text from a list of possible labels. A typical use case is aspect categories detection where one want to detect the multiple aspects mentionned in a review (e.g., product_quality, delivery_time, price, ...).
* **Aspect-based classification** [Not yet implemented]: Assign one label from a list of possible labels for each of a list of aspects. A typical use case is aspect based sentiment analysis where one want to detect each aspect categories mentionned in a review along his assocated sentiment polarity (e.g., product_quality: neutral, delivery_time: negative, price: positive, ...).

`NLPipes` expose a simple `Model` API that offers a common abstraction to run several text classification tasks. The `Model` encapsulate most of the complex code from the library and save having to deal with the complexity of transformers based algorithms.

#### Built with
`NLPipes` is built with TensorFlow and HuggingFace Transformers:
* [TensorFlow](https://www.tensorflow.org/): An end-to-end open source deep learning framework
* [Transformers](https://huggingface.co/transformers/): An general-purpose open-sources library for transformers-based architectures

## Getting Started

#### Installation
1. Create a virtual environment

 ```console
 python3 -m venv nlpipesenv
 source nlpipesenv/bin/activate
 ```

2. Install the package

 ```console
 pip install nlpipes
 ```

#### Tutorials

Here are some examples on open datasets that show how to use `NLPipes` on different tasks:

Name|Notebook|Description|Task|Size|Memory|Speed| 
----|-----------|-----|---------|---------|---------|---------|
GooglePlay Sentiment Detection|Available|Train a model to detect the sentiment polarity from the GooglePlay store |Single-label classification|  |  |  
StackOverflow tags Detection|Available|Train a model to detect tags from the StackOverFlow questions |Multiple-labels classification|  |  |
GooglePlay Aspect and Sentiment Detection|Coming soon|Train a model to detect the aspects from GooglePlay store reviews along their assocated sentiment polarity |Aspect-based classification|  |  | 




#### Why should I use NLPipes?
- End to End solution for practical text classification problems, especially in the context of aspect based sentiment analysis.
- Low barrier to entry. Given the unified API for all classification task, there is just one abstraction to learn.
- Flexible architecture. Most of nlpipes functionnalities are based on callbacks function. This allows new research to be implemented without having to increase the complexity of the core. 


#### Why shouldn’t I use NLPipes?
- Nlpipes is not intended to provide building blocks to create customized transformer-based neural network.
- Speed and mermory footprint efficiency will improve in the future, but if you're looking for an high performance library for training and inference, there is probably better alternatives.


## Notice
`NLPipes` is still in its early stage and not yet suitable for production usage. The library comes with no warranty as future releases could bring substantial API and behavior changes.


<div>Logo created with <a href="https://www.designevo.com/" title="Free Online Logo Maker">DesignEvo logo maker</a></div>
