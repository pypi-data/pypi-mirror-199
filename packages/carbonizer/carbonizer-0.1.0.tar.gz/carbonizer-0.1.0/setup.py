# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['carbonizer']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.6.0,<0.7.0', 'pyppeteer>=1.0.2,<2.0.0']

entry_points = \
{'console_scripts': ['greet = carbonizer.cli:carbonize']}

setup_kwargs = {
    'name': 'carbonizer',
    'version': '0.1.0',
    'description': 'A Small CLI to utilize Carbon.now.sh',
    'long_description': '',
    'author': 'marvin taschenberger',
    'author_email': 'marvin.taschenberger@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
