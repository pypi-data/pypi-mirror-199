# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['faudantic']

package_data = \
{'': ['*']}

install_requires = \
['faunadb>=4.5.0,<5.0.0', 'pydantic[dotenv]>=1.10.7,<2.0.0']

setup_kwargs = {
    'name': 'faudantic',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Oscar Bahamonde',
    'author_email': '107950590+obahamonde@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
