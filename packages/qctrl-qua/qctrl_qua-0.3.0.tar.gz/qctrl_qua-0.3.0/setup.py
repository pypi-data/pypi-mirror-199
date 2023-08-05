# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qctrlqua']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.0,<2.0.0']

setup_kwargs = {
    'name': 'qctrl-qua',
    'version': '0.3.0',
    'description': 'Q-CTRL Python QUA',
    'long_description': '# Q-CTRL QUA\n\nThe Q-CTRL QUA Python package allows you to integrate Boulder Opal with the QUA\nquantum computing language.\n',
    'author': 'Q-CTRL',
    'author_email': 'support@q-ctrl.com',
    'maintainer': 'Q-CTRL',
    'maintainer_email': 'support@q-ctrl.com',
    'url': 'https://q-ctrl.com',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
