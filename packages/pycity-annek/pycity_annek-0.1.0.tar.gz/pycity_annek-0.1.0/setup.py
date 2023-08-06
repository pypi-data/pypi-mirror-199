# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pycity_annek']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'requests>=2.28.2,<3.0.0', 'termcolor>=2.2.0,<3.0.0']

entry_points = \
{'console_scripts': ['pycity = pycity_annek.cli:pycity']}

setup_kwargs = {
    'name': 'pycity-annek',
    'version': '0.1.0',
    'description': 'CLI for TeamCity API Requests',
    'long_description': '=====================\nPyCity\n=====================\n\nCLI for making requests to TeamCity\n',
    'author': 'Michael MacKenna',
    'author_email': 'mmackenna@ufginsurance.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
