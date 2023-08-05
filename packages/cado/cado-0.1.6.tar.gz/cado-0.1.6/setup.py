# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cado', 'cado.app', 'cado.cli', 'cado.core', 'cado.examples']

package_data = \
{'': ['*'],
 'cado': ['ui/*',
          'ui/dist/*',
          'ui/dist/assets/*',
          'ui/public/*',
          'ui/src/*',
          'ui/src/components/*',
          'ui/src/hooks/*',
          'ui/src/images/*',
          'ui/src/lib/*',
          'ui/src/lib/models/*',
          'ui/src/widgets/*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'fastapi>=0.70.0,<0.71.0',
 'pydantic>=1.9.0,<2.0.0',
 'uvicorn[standard]>=0.15.0,<0.16.0']

entry_points = \
{'console_scripts': ['cado = cado.cli.cli:main']}

setup_kwargs = {
    'name': 'cado',
    'version': '0.1.6',
    'description': 'Python notebook development environment.',
    'long_description': '<div align="center">\n  <img src="assets/cado-banner.png">\n  <h1>cado</h1>\n\n  <p>\n    <strong>Python notebook IDE with a focus on reactivity</strong>\n  </p>\n\n  <br>\n  <div>\n    <a href="https://badge.fury.io/py/cado"><img src="https://badge.fury.io/py/cado.svg" alt="PyPI"></a>\n    <a href="https://pepy.tech/project/cado"><img src="https://pepy.tech/badge/cado" alt="Downloads"></a>\n    <a href="https://github.com/gregorybchris/cado/actions/workflows/ci.yaml"><img src="https://github.com/gregorybchris/cado/actions/workflows/ci.yaml/badge.svg" alt="CI"></a>\n  </div>\n  <br>\n</div>\n\n## About\n\n`cado` is a notebook IDE for Python, like [Jupyter](https://jupyter.org/), but with a reactive cell model, taking inspiration from [Observable](https://observablehq.com/). Each cell defines its own outputs that other cells can listen to. When a child cell runs, it uses cached outputs from parent cells. And when the output of a parent cell updates, the change propagates to all child cells automatically.\n\n## Installation\n\n```bash\npip install cado\n```\n\n## Usage\n\n```bash\n# Start up a cado server\ncado up\n\n# Open http://0.0.0.0:8000 in a browser\n```\n\nYou should now see a screen that lists out all of your notebooks. Click on the example notebook to get started.\n\n<p align="center">\n  <img style="inline-block; margin-right: 10px;" src="assets/notebooks-screen.png" height=400>\n  <img style="inline-block" src="assets/notebook-screen.png" height=400>\n</p>\n\n## Keyboard Shortcuts\n\n| Action                                       | Command        |\n| -------------------------------------------- | -------------- |\n| Make the cell above the active cell          | `UpArrow`      |\n| Make the cell below the active cell          | `DownArrow`    |\n| Run the active cell                          | `Shift+Enter`  |\n| Clear the active cell                        | `Shift+Delete` |\n| Turn on edit mode                            | `Enter`        |\n| Turn off edit mode                           | `Escape`       |\n| Create a new cell before the active cell     | `Control+a`    |\n| Create a new cell after the active cell      | `Control+b`    |\n| Create a new cell at the end of the notebook | `Control+n`    |\n| Delete the active cell                       | `Control+d`    |\n\n## Features\n\nIf you have ideas for new features feel free to create an issue or submit a pull request!\n\n- [x] Reactive cells\n- [x] Auto-save to disk\n- [x] Keyboard shortcuts\n- [x] Drag cells to reorder\n- [x] Markdown mode\n- [x] Notebook files viewer\n',
    'author': 'Chris Gregory',
    'author_email': 'christopher.b.gregory@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/gregorybchris/cado',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<4',
}


setup(**setup_kwargs)
