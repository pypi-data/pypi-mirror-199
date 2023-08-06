# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['casing']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'casing',
    'version': '1.0.12',
    'description': 'Easy casing nomenclatures management such as camelCase, snake_case and many others!',
    'long_description': '# casing\n\n[![Build Status](https://travis-ci.org/vincentBenet/casing.svg?branch=main)](https://travis-ci.org/vincentBenet/casing)\n[![Coverage Status](https://coveralls.io/repos/github/vincentBenet/casing/badge.svg)](https://coveralls.io/github/vincentBenet/casing)\n',
    'author': 'vincentBenet',
    'author_email': 'vincent.benet@outlook.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
