# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['intellifire4py']

package_data = \
{'': ['*']}

install_requires = \
['aenum>=3.1.11,<4.0.0',
 'httpx>=0.23.0,<0.24.0',
 'pydantic>=1.10.2,<2.0.0',
 'rich==10.16.2']

entry_points = \
{'console_scripts': ['intellifire4py = intellifire4py.__main__:main']}

setup_kwargs = {
    'name': 'intellifire4py',
    'version': '3.1.5',
    'description': 'Intellifire4Py',
    'long_description': "# Intellifire4Py\n\n[![PyPI](https://img.shields.io/pypi/v/intellifire4py.svg)][pypi_]\n[![Status](https://img.shields.io/pypi/status/intellifire4py.svg)][status]\n[![Python Version](https://img.shields.io/pypi/pyversions/intellifire4py)][python version]\n[![License](https://img.shields.io/pypi/l/intellifire4py)][license]\n\n[![Read the documentation at https://intellifire4py.readthedocs.io/](https://img.shields.io/readthedocs/intellifire4py/latest.svg?label=Read%20the%20Docs)][read the docs]\n[![Tests](https://github.com/jeeftor/intellifire4py/workflows/Tests/badge.svg)][tests]\n[![Codecov](https://codecov.io/gh/jeeftor/intellifire4py/branch/main/graph/badge.svg)][codecov]\n\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]\n\n[pypi_]: https://pypi.org/project/intellifire4py/\n[status]: https://pypi.org/project/intellifire4py/\n[python version]: https://pypi.org/project/intellifire4py\n[read the docs]: https://intellifire4py.readthedocs.io/\n[tests]: https://github.com/jeeftor/intellifire4py/actions?workflow=Tests\n[codecov]: https://app.codecov.io/gh/jeeftor/intellifire4py\n[pre-commit]: https://github.com/pre-commit/pre-commit\n[black]: https://github.com/psf/black\n\n## Features\n\n- TODO\n\n## Requirements\n\n- TODO\n\n## Installation\n\nYou can install _Intellifire4Py_ via [pip] from [PyPI]:\n\n```console\n$ pip install intellifire4py\n```\n\n## Usage\n\nPlease see the [API Reference] for details.\n\n## Contributing\n\nContributions are very welcome.\nTo learn more, see the [Contributor Guide].\n\n## License\n\nDistributed under the terms of the [MIT license][license],\n_Intellifire4Py_ is free and open source software.\n\n## Issues\n\nIf you encounter any problems,\nplease [file an issue] along with a detailed description.\n\n## Credits\n\nThis project was generated from [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.\n\n[@cjolowicz]: https://github.com/cjolowicz\n[pypi]: https://pypi.org/\n[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python\n[file an issue]: https://github.com/jeeftor/intellifire4py/issues\n[pip]: https://pip.pypa.io/\n\n<!-- github-only -->\n\n[license]: https://github.com/jeeftor/intellifire4py/blob/main/LICENSE\n[contributor guide]: https://github.com/jeeftor/intellifire4py/blob/main/CONTRIBUTING.md\n[command-line reference]: https://intellifire4py.readthedocs.io/en/latest/usage.html\n",
    'author': 'Jeff Stein',
    'author_email': 'jeffstein@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jeeftor/intellifire4py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
