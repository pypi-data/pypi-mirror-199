# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_commons_exceptions']

package_data = \
{'': ['*']}

install_requires = \
['fastapi>=0.95.0,<0.96.0']

setup_kwargs = {
    'name': 'fastapi-commons-exceptions',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'ventura94',
    'author_email': 'arianventura94@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
