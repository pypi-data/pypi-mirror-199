# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anime_autodownloader']

package_data = \
{'': ['*']}

install_requires = \
['filelock>=3.10.4,<4.0.0',
 'requests>=2.28.2,<3.0.0',
 'selenium>=4.8.2,<5.0.0',
 'uuid-by-string>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'anime-autodownloader',
    'version': '0.0.1',
    'description': 'A package for downloading animes automatically from a given streaming website',
    'long_description': None,
    'author': 'Luca Paganin',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
