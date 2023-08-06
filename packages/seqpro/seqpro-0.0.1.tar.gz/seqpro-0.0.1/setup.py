# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['seqpro']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21.5,<2.0.0', 'torch>=1.11.0,<2.0.0']

setup_kwargs = {
    'name': 'seqpro',
    'version': '0.0.1',
    'description': 'Sequence preprocessing toolkit',
    'long_description': None,
    'author': 'adamklie',
    'author_email': 'aklie@ucsd.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
