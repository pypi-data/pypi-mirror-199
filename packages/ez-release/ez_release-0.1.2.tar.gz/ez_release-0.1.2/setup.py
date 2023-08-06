# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['release', 'release.cli']

package_data = \
{'': ['*']}

install_requires = \
['gitpython>=3.1.31,<4.0.0',
 'pydantic>=1.10.5,<2.0.0',
 'pyyaml>=6.0,<7.0',
 'semver>=2.13.0,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['release = release.cli.main:app']}

setup_kwargs = {
    'name': 'ez-release',
    'version': '0.1.2',
    'description': 'Make release easier with git and semver tags.',
    'long_description': 'None',
    'author': 'dithyrambe',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
