# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydit', 'pydit.functions']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib',
 'numpy>=1.24,<2.0',
 'openpyxl>=3.0.0,<4.0.0',
 'pandas>=1.5.0,<2.0.0']

setup_kwargs = {
    'name': 'pydit-jceresearch',
    'version': '0.0.12',
    'description': 'Data cleansing tools for Internal Auditors',
    'long_description': None,
    'author': 'jceresearch',
    'author_email': 'jceresearch@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
