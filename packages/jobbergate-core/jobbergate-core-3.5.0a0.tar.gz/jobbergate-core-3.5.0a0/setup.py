# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jobbergate_core', 'jobbergate_core.auth']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.22.0,<0.23.0',
 'loguru>=0.6.0,<0.7.0',
 'pendulum>=2.1.2,<3.0.0',
 'py-buzz>=3.1.0,<4.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'python-jose>=3.3.0,<4.0.0']

setup_kwargs = {
    'name': 'jobbergate-core',
    'version': '3.5.0a0',
    'description': 'Jobbergate Core',
    'long_description': '=================\n Jobbergate Core\n=================\n\nJobbergate-core is a sub-project that contains the key components and logic that is shared among all other sub-projects (CLI, API, and Agent). Additionally, jobbergate-core exists to support custom automation built on top of Jobbergate.\n\nLicense\n-------\n* `MIT <LICENSE>`_\n\n\nCopyright\n---------\n* Copyright (c) 2023 OmniVector Solutions <info@omnivector.solutions>\n\n',
    'author': 'Omnivector Solutions',
    'author_email': 'info@omnivector.solutions',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/omnivector-solutions/jobbergate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
