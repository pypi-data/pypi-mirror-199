# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lenskappa',
 'lenskappa.analysis',
 'lenskappa.catalog',
 'lenskappa.counting',
 'lenskappa.datasets',
 'lenskappa.datasets.simulations',
 'lenskappa.datasets.surveys',
 'lenskappa.datasets.surveys.ms',
 'lenskappa.output',
 'lenskappa.plugin',
 'lenskappa.test',
 'lenskappa.tests',
 'lenskappa.tests.output',
 'lenskappa.utils',
 'lenskappa.weighting']

package_data = \
{'': ['*'],
 'lenskappa': ['config/*', 'config/analysis/*'],
 'lenskappa.tests': ['0029/*'],
 'lenskappa.weighting': ['config/*']}

install_requires = \
['Shapely>=1.8.1,<2.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'astropy>=5.0.3,<6.0.0',
 'heinlein>=0.4.0,<0.5.0',
 'multiprocess>=0.70.13,<0.71.0',
 'networkx>=3.0,<4.0',
 'numpy>=1.22.3,<2.0.0',
 'pandas>=1.4.1,<2.0.0',
 'regions==0.7',
 'scipy>=1.8.0,<2.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['lenskappa_inference = '
                     'lenskappa.analysis.run_inference:run_inference']}

setup_kwargs = {
    'name': 'lenskappa',
    'version': '0.5.1',
    'description': '',
    'long_description': 'None',
    'author': 'Patrick Wells',
    'author_email': 'pwells@ucdavis.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
