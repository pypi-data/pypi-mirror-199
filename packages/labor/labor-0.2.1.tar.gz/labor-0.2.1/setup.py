# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['labor', 'labor.controllers', 'labor.enums', 'labor.services', 'labor.utils']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'colorama>=0.4.3,<0.5.0',
 'httpx>=0.23.0,<0.24.0',
 'rich>=12.4.4,<13.0.0',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['labor = labor.cli:cli']}

setup_kwargs = {
    'name': 'labor',
    'version': '0.2.1',
    'description': 'getLabor cli',
    'long_description': None,
    'author': 'Gabriel Santo',
    'author_email': 'gabssanto@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gabssanto/labor-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
