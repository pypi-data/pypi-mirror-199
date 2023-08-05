# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chainingiterator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chainingiterator',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Adam Ruman',
    'author_email': 'ruman.adam@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
