# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['convnets',
 'convnets.datasets',
 'convnets.models',
 'convnets.models.lenet',
 'convnets.models.resnet',
 'convnets.models.vgg',
 'convnets.train']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'convnets',
    'version': '0.2.8',
    'description': 'Convolutional Neural Networks and utilities for Computer Vision',
    'long_description': "# convnets\n\n🚧 Under construction\n\nConvolutional Neural Networks and utilities for Computer Vision.\n\n- [Learn](learn) about convnets.\n- Learn about popular [models](models).\n\n## Models API\n\n`convnets` offers implementations for the following models:\n\n- [LeNet](http://vision.stanford.edu/cs598_spring07/papers/Lecun98.pdf)\n- [AlexNet](https://proceedings.neurips.cc/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf)\n- [VGG](https://arxiv.org/abs/1409.1556)\n- [ResNet](https://arxiv.org/abs/1512.03385)\n\nTo instantiate a model you need to import the corresponding class and pass a valid `configuration` object to the constructor:\n\n```python\nfrom convnets.models import ResNet\n\nr18_config = {\n\t'l': [\n\t\t{'r': 2, 'f': 64},\n\t\t{'r': 2, 'f': 128},\n\t\t{'r': 2, 'f': 256},\n\t\t{'r': 2, 'f': 512}\n\t], \n\t'b': False\n}\n\nmodel = ResNet(r18_config)\n```\n\nOr you can use one of the predefined configurations, or variants:\n\n```python\nfrom convnets.models import ResNet, ResNetConfig\n\nmodel = ResNet(ResNetConfig.r18)\n```\n\nYou can find the implementation of each model and configuration examples in the [`convnets/models`](convnets/models) directory.\n\n## Training API\n\nIf you want to train a model in your notebooks, you can use our [fit](convents/train/fit.py) function:\n\n```python\nform convnets.train import fit \n\nhist = fit(model, dataloader, optimizer, criterion, metrics, max_epochs)\n```\n\nYou can use any Pytorch model. You will need to define the Pytorch dataloader, optimizer and criterion. For the metrics, the function expects a dict with the name of the metric as key and the metric function as value. The metric function must receive the model output and the target and return a scalar value. You can find some examples in [`convnets/metrics`](convnets/metrics.py). The `max_epochs` parameter is the maximum number of epochs to train the model. The function will return a dict with the training history. \n\nAdditionally, we offer a [training script](train/train.py) that you can execute from the command line.\n\n```bash\npython scripts/train.py <path_to_config_file>\n```\n\nYou will have to pass the path to a yaml file with the configuration for your training, including the model, optimizer, criterion, metrics, dataloader, etc. You can find some examples in the [`configs`](scripts/configs) directory (which are `timm` and `pytorch-lightning` compatible).\n\nWe also offer Pytorch Lightning interoperability.",
    'author': 'juansensio',
    'author_email': 'sensio.juan@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
