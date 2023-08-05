# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['osdi', 'osdi.action_builder', 'osdi.action_network', 'osdi.base']

package_data = \
{'': ['*']}

install_requires = \
['flake8==5.0.4', 'isort>=5.11.4,<6.0.0', 'requests>=2.20.0,<3.0.0']

setup_kwargs = {
    'name': 'osdi',
    'version': '0.3.1',
    'description': 'A library for interacting with OSDI-descended services, namely ActionNetwork and ActionBuilder',
    'long_description': 'None',
    'author': 'Tal L',
    'author_email': 'tal42levy@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
