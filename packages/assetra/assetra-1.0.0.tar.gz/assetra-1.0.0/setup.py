# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['assetra']

package_data = \
{'': ['*']}

install_requires = \
['netCDF4>=1.6.2,<2.0.0',
 'numpy>=1.24.2,<2.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.4.4,<2.0.0',
 'xarray>=2023.2.0,<2024.0.0']

setup_kwargs = {
    'name': 'assetra',
    'version': '1.0.0',
    'description': 'ASSET Lab Resource Adequacy Package',
    'long_description': '=======\nASSETRA\n=======\n\n.. image:: https://img.shields.io/pypi/v/assetra.svg\n        :target: https://pypi.python.org/pypi/assetra\n\n.. image:: https://readthedocs.org/projects/assetra/badge/?version=latest\n        :target: https://assetra.readthedocs.io/en/latest/?version=latest\n        :alt: Documentation Status\n\n\nThe ASSET Lab Resource adequacy package (assetra) is a light-weight, open-source energy system resource adequacy package maintained by the University of Michigan ASSET Lab.\n\n\n* Free software: MIT license\n* Documentation: https://assetra.readthedocs.io.\n\n\nFeatures\n--------\n* Probabilistic Monte Carlo state-sampling simulation framework, supporting:\n        * Time-varying forced outage rates in thermal units\n        * Sequential storage unit dispatch\n        * User-defined energy unit types\n* Resource adequacy calculation:\n        * Expected unserved energy (EUE)\n        * Loss of load hours (LOLH)\n        * Loss of load days (LOLD)\n        * Loss of load frequency (LOLF)\n* Resource contribution calculation:\n        * Effective load-carrying capability (ELCC)\n* Object-oriented interface to manage energy units within energy systems\n* Internal computation stored in `xarray <https://docs.xarray.dev/en/stable/index.html>`_ datasets\n\nFuture Work\n-----------\n* Regional interchange and transmission\n* Parallelized computation\n\nCredits\n-------\nThis package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage\n',
    'author': 'Isaac Bromley-Dulfano',
    'author_email': 'ijbd@umich.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
