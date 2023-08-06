# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['evmrpc']

package_data = \
{'': ['*']}

install_requires = \
['web3>=6.0.0,<7.0.0']

setup_kwargs = {
    'name': 'evmrpc',
    'version': '0.2.1',
    'description': 'A library for batching Ethereum RPC calls',
    'long_description': None,
    'author': 'Fed',
    'author_email': 'federicoulfo@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
