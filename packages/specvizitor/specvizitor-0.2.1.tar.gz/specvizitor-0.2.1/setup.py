# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['specvizitor',
 'specvizitor.config',
 'specvizitor.io',
 'specvizitor.menu',
 'specvizitor.plugins',
 'specvizitor.utils',
 'specvizitor.widgets']

package_data = \
{'': ['*'],
 'specvizitor': ['data/*', 'data/icons/dark/*', 'data/icons/light/*']}

install_requires = \
['astropy>=5.2.1,<6.0.0',
 'dacite>=1.8.0,<2.0.0',
 'dictdiffer>=0.9.0,<0.10.0',
 'pandas>=1.5.3,<2.0.0',
 'pgcolorbar>=1.1.3,<2.0.0',
 'pillow>=9.4.0,<10.0.0',
 'platformdirs>=3.0.0,<4.0.0',
 'pyqt5>=5.15.9,<6.0.0',
 'pyqtdarktheme>=2.1.0,<3.0.0',
 'pyqtgraph>=0.13.1,<0.14.0',
 'qtpy>=2.3.0,<3.0.0',
 'scipy>=1.10.1,<2.0.0',
 'specutils>=1.9.1,<2.0.0']

entry_points = \
{'console_scripts': ['specvizitor = specvizitor.gui:main']}

setup_kwargs = {
    'name': 'specvizitor',
    'version': '0.2.1',
    'description': 'Python GUI application for a visual inspection of astronomical spectroscopic data',
    'long_description': '![Specvizitor GUI](https://github.com/ivkram/specvizitor/blob/main/docs/screenshots/specvizitor_gui.png?raw=true "Specvizitor GUI")\n\n## Installation\n\n### Installing `specvizitor` using pip\n\nSet up a local environment and run\n\n        $ pip install specvizitor\n\n### Installing `specvizitor` from source\n\n1. Clone the public repository:\n\n        $ git clone https://github.com/ivkram/specvizitor\n        $ cd specvizitor\n\n2. Set up a local environment and run\n\n        $ pip install -e .\n\n## Starting `specvizitor`\n    \nTo start `specvizitor`, run this command in your terminal:\n\n    $ specvizitor\n\n## Troubleshooting\n\nTo reset `specvizitor` to its initial state, run the script with the `--purge` option:\n\n    $ specvizitor --purge\n\n## License\n\n`specvizitor` is licensed under a 3-clause BSD style license - see the [LICENSE.txt](https://github.com/ivkram/specvizitor/blob/main/LICENSE.txt) file.',
    'author': 'Ivan Kramarenko',
    'author_email': 'im.kramarenko@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ivkram/specvizitor',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
