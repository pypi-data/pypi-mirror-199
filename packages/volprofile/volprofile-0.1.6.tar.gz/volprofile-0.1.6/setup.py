# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['volprofile']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.23.4,<2.0.0', 'pandas>=1.5.1,<2.0.0', 'plotly>=5.11.0,<6.0.0']

setup_kwargs = {
    'name': 'volprofile',
    'version': '0.1.6',
    'description': 'calculate the volume profile in a flexible manner!',
    'long_description': '`pip install volprofile`\n',
    'author': 'maghrebi',
    'author_email': 'sajad.faghfoor@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.x,<4',
}


setup(**setup_kwargs)
