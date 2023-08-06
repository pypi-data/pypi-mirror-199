# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['type_inspector']

package_data = \
{'': ['*']}

install_requires = \
['issubclass>=0.1.2']

setup_kwargs = {
    'name': 'type-inspector',
    'version': '1.1.0',
    'description': '',
    'long_description': 'None',
    'author': 'Stanislav Zmiev',
    'author_email': 'szmiev2000@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
