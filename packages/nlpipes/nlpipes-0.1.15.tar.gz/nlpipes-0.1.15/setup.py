# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nlpipes',
 'nlpipes.callbacks',
 'nlpipes.configurations',
 'nlpipes.data',
 'nlpipes.layers',
 'nlpipes.losses',
 'nlpipes.metrics',
 'nlpipes.models',
 'nlpipes.optimization',
 'nlpipes.pipelines',
 'nlpipes.trainers']

package_data = \
{'': ['*']}

install_requires = \
['ftfy>=6.1.1,<7.0.0',
 'numpy>=1.21.0,<2.0.0',
 'pandas>=1.3.5,<2.0.0',
 'scipy>=1.7.3,<2.0.0',
 'tensorflow>=2.11.0,<3.0.0',
 'tokenizers>=0.13.0,<0.14.0',
 'tqdm>=4.64.0,<5.0.0',
 'transformers>=4.24.0,<5.0.0']

setup_kwargs = {
    'name': 'nlpipes',
    'version': '0.1.15',
    'description': 'Text Classification with Transformers',
    'long_description': '<!-- PROJECT NAME -->\n<div align="center">\n   <img src="https://raw.githubusercontent.com/uyanik/Images/b90c13ff8e580b2ecb2468889ed5ab1d52633d2e/logo.png" alt="nlpipes_logo" title="nlpipes logo">\n  <h2>Text Classification with Transformers</h2>\n</div>\n\n<div align="center">\n    <a href="https://opensource.org/licenses/Apache-2.0">\n       <img alt="Licence" src="https://img.shields.io/badge/License-Apache_2.0-blue.svg">\n    </a>\n     <a href="https://pypi.org/project/nlpipes/">\n       <img alt="PyPi Version" src="https://img.shields.io/pypi/pyversions/nlpipes">\n    </a> \n    <a href="https://pypi.org/project/nlpipes/">\n        <img alt="PyPi Package Version" src="https://img.shields.io/pypi/v/nlpipes">\n    </a>\n    <!--\n    <a href="https://pepy.tech/project/nlpipes/">\n        <img alt="PyPi Downloads" src="https://static.pepy.tech/badge/nlpipes/month">\n    </a>\n    -->\n</div>\n\n<div align="center">\n    <a href=""><strong>Documentation</strong></a>\n    • <a href=""><strong>References</strong></a>\n</div>\n\n\n<div align="center">\n  <img src="https://ik.imagekit.io/m0ci8dgk4/nlpipes_screenshot_w_309qBjx.png?ik-sdk-version=javascript-1.4.3&updatedAt=1678033602383" alt="nlpipes_screenshot" title="nlpipes screenshot">\n</div>\n\n\n## Overview\n`NLPipes` provides an easy way to use Transformers-based models for training, evaluation and inference on a diversity of text classification tasks, including:\n\n* **Single-label classification**: Assign one label to each text. A typical use case is sentiment detection where one want to detect the overall sentiment polarity (e.g., positive, neutral, negative) in a review.\n* **Multi-labels classification**: Assign one or more label to each text from a list of possible labels. A typical use case is aspect categories detection where one want to detect the multiple aspects mentionned in a review (e.g., product_quality, delivery_time, price, ...).\n* **Aspect-based classification** [Not yet implemented]: Assign one label from a list of possible labels for each of a list of aspects. A typical use case is aspect based sentiment analysis where one want to detect each aspect categories mentionned in a review along his assocated sentiment polarity (e.g., product_quality: neutral, delivery_time: negative, price: positive, ...).\n\n`NLPipes` expose a simple `Model` API that offers a common abstraction to run several text classification tasks. The `Model` encapsulate most of the complex code from the library and save having to deal with the complexity of transformers based algorithms.\n\n#### Built with\n`NLPipes` is built with TensorFlow and HuggingFace Transformers:\n* [TensorFlow](https://www.tensorflow.org/): An end-to-end open source deep learning framework\n* [Transformers](https://huggingface.co/transformers/): An general-purpose open-sources library for transformers-based architectures\n\n## Getting Started\n\n#### Installation\n1. Create a virtual environment\n\n ```console\n python3 -m venv nlpipesenv\n source nlpipesenv/bin/activate\n ```\n\n2. Install the package\n\n ```console\n pip install nlpipes\n ```\n\n#### Tutorials\n\nHere are some examples on open datasets that show how to use `NLPipes` on different tasks:\n\nName|Notebook|Description|Task|Size|Memory|Speed| \n----|-----------|-----|---------|---------|---------|---------|\nGooglePlay Sentiment Detection|Available|Train a model to detect the sentiment polarity from the GooglePlay store |Single-label classification|  |  |  \nStackOverflow tags Detection|Available|Train a model to detect tags from the StackOverFlow questions |Multiple-labels classification|  |  |\nGooglePlay Aspect and Sentiment Detection|Coming soon|Train a model to detect the aspects from GooglePlay store reviews along their assocated sentiment polarity |Aspect-based classification|  |  | \n\n\n\n\n#### Why should I use NLPipes?\n- End to End solution for practical text classification problems, especially in the context of aspect based sentiment analysis.\n- Low barrier to entry. Given the unified API for all classification task, there is just one abstraction to learn.\n- Flexible architecture. Most of nlpipes functionnalities are based on callbacks function. This allows new research to be implemented without having to increase the complexity of the core. \n\n\n#### Why shouldn’t I use NLPipes?\n- Nlpipes is not intended to provide building blocks to create customized transformer-based neural network.\n- Speed and mermory footprint efficiency will improve in the future, but if you\'re looking for an high performance library for training and inference, there is probably better alternatives.\n\n\n## Notice\n`NLPipes` is still in its early stage and not yet suitable for production usage. The library comes with no warranty as future releases could bring substantial API and behavior changes.\n\n\n<div>Logo created with <a href="https://www.designevo.com/" title="Free Online Logo Maker">DesignEvo logo maker</a></div>\n',
    'author': 'Ayhan UYANIK',
    'author_email': 'ayhan.uyanik@renault.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
