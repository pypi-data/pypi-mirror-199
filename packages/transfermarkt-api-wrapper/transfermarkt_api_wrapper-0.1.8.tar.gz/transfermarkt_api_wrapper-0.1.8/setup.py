# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transfermarkt_api_wrapper',
 'transfermarkt_api_wrapper.clubs',
 'transfermarkt_api_wrapper.competitions',
 'transfermarkt_api_wrapper.pandas',
 'transfermarkt_api_wrapper.pandas.competitions',
 'transfermarkt_api_wrapper.pandas.players',
 'transfermarkt_api_wrapper.players']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.3,<2.0.0', 'requests>=2.28.2,<3.0.0', 'tqdm>=4.65.0,<5.0.0']

setup_kwargs = {
    'name': 'transfermarkt-api-wrapper',
    'version': '0.1.8',
    'description': 'Lightweight wrapper for Transfermarkt API',
    'long_description': '# transfermarkt-api-wrapper',
    'author': 'Felipe Allegretti',
    'author_email': 'felipe@allegretti.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
