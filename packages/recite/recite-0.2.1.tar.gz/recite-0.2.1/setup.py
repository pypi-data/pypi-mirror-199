# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['recite']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['gitpython>=3.1.30,<4.0.0',
 'rich>=13.1.0,<14.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer>=0.7.0,<0.8.0']

extras_require = \
{'docs': ['mkdocs>=1.4.2,<2.0.0', 'mkdocs-material>=9.0.9,<10.0.0']}

entry_points = \
{'console_scripts': ['recite = recite.main:app']}

setup_kwargs = {
    'name': 'recite',
    'version': '0.2.1',
    'description': 'Publish your poetry-based projects, without missing important steps',
    'long_description': '<p align="center">\n<img src="https://github.com/dobraczka/recite/raw/main/docs/assets/logo.png" alt="recite logo", width=200/>\n</p>\n<h2 align="center"> recite</h2>\n\n\n<p align="center">\n<a href="https://github.com/dobraczka/recite/actions/workflows/main.yml"><img alt="Actions Status" src="https://github.com/dobraczka/recite/actions/workflows/main.yml/badge.svg?branch=main"></a>\n<a href=\'https://recite.readthedocs.io/en/latest/?badge=latest\'><img src=\'https://readthedocs.org/projects/recite/badge/?version=latest\' alt=\'Documentation Status\' /></a>\n<a href="https://codecov.io/gh/dobraczka/recite"><img src="https://codecov.io/gh/dobraczka/recite/branch/main/graph/badge.svg?token=TCMKS9U0MH"/></a>\n<a href="https://pypi.org/project/recite"/><img alt="Stable python versions" src="https://img.shields.io/pypi/pyversions/recite"></a>\n<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\n`recite` intends to make releasing [poetry](https://python-poetry.org/)-based libraries easier and avoid missing important steps (e.g. adapting the changelog (because [you should keep one](https://keepachangelog.com/))).\n\n```console\n$ recite release patch\n\nrecite > 👀 Checking everything to make sure you are ready to release 👀\nrecite > 1: ✓ Make sure you have a (non-empty) pyproject.toml\nrecite > 2: ✓ Make sure you\'re on main/master branch\nrecite > 3: ✓ Make sure git is clean\nrecite > 4: ✓ Run test-suite\nrecite > 5: ✓ Make sure changelog was updated\nrecite > 🤓 Everything looks perfect! 🤓\nrecite > I will perform the following steps:\nrecite >        * Would bump version from 0.1.0 to 0.1.1\nrecite >        * Commit version bump\nrecite >        * Create git tag 0.1.1\nrecite >        * Push git tag 0.1.1\nrecite >        * Remind you to upload build as github release\nDo you want to proceed? [y/N]: y\nrecite > ✨ Performing release ✨\nrecite > 1: ✓ Bump version\nrecite >        * Bumped version from 0.1.0 to 0.1.1\nrecite > 2: ✓ Commit version bump\nrecite > 3: ✓ Create git tag 0.1.1\nrecite > 4: ✓ Push git tag 0.1.1\nrecite > 5: ✓ Build and publish with poetry\nPlease create a github release now! Did you do it? [y/N]: y\nrecite > 6: ✓ Remind you to upload build as github release\nrecite > 🚀 Congrats to your release! 🚀\n```\n\n# Installation\n\nSince `recite` is a python application it is recommended to install it via [pipx](https://pypa.github.io/pipx/):\n```console\n$ pipx install recite\n```\n\nBut you can also install it via pip:\n\n```console\n$ pip install recite\n```\n\n# Usage\n\nYou can perform e.g a patch release with the command:\n\n```console\n$ recite release patch\n```\n\nThe classifiers are the same as poetry\'s bump rules of the it\'s [version command](https://python-poetry.org/docs/cli/#version).\n\nTo list the available checks use:\n\n```console\n$ recite list-checks\n```\n\nYou can find more info in the [docs](https://recite.readthedocs.io)\n\n# Why?\n\nPreviously I used a github action to automatically build and publish a new version of a library if a new tag was pushed. However, sometimes I forgot something crucial (e.g. to adapt the changelog). In this case I had to rush to stop the github action before it would publish the release to pypi (where it would lie forever unable to be rectified).\nWith `recite` it is ensured all the necessary checks are in place before any tags are created.\n',
    'author': 'Daniel Obraczka',
    'author_email': 'obraczka@informatik.uni-leipzig.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/dobraczka/recite',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
