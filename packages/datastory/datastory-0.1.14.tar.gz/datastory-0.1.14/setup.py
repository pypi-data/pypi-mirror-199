# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datastory']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'datastory',
    'version': '0.1.14',
    'description': '',
    'long_description': None,
    'author': 'nada developers',
    'author_email': 'nada@nav.no',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
