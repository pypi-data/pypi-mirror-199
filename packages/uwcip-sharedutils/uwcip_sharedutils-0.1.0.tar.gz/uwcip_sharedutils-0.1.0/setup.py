# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sharedutils']

package_data = \
{'': ['*']}

install_requires = \
['pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'uwcip-sharedutils',
    'version': '0.1.0',
    'description': '',
    'long_description': '# sharedutils\nCode under **sharedutils** are a collection of common functions shared by all projects\n',
    'author': 'Lia Bozarth',
    'author_email': 'liafan@uw.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
