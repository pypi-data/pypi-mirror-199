# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymaxed']

package_data = \
{'': ['*']}

install_requires = \
['pyapes>=0.2.1,<0.3.0']

setup_kwargs = {
    'name': 'pymaxed',
    'version': '0.1.7',
    'description': 'Python package for the maximum entroy distribution.',
    'long_description': 'None',
    'author': 'Kyoungseoun Chung',
    'author_email': 'kyoungseoun.chung@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
