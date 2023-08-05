# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chainingiterator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chainingiterator',
    'version': '0.1.5',
    'description': "A python wrapper-library for iterators to be usable via chaining(such as C#, Java streams or Rust iterators). Extended functionality based on Rust's buit-in iterators.",
    'long_description': "# chainingiterator\nA python wrapper-library for iterators to be usable via chaining(such as C#, Java streams or Rust iterators). Extended functionality based on Rust's buit-in iterators. \n",
    'author': 'Adam Ruman',
    'author_email': 'ruman.adam@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/addam128/chainingiterator',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
