# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['anoexpress']

package_data = \
{'': ['*']}

install_requires = \
['malariagen_data',
 'numpy',
 'plotly',
 'scipy',
 'seaborn',
 'statsmodels',
 'tqdm']

extras_require = \
{':python_full_version >= "3.7.1" and python_version < "3.8"': ['pandas<1.4'],
 ':python_version >= "3.8" and python_version < "3.11"': ['pandas']}

setup_kwargs = {
    'name': 'anoexpress',
    'version': '0.1.2',
    'description': 'A package to access insecticide resistance gene expression meta analyse in Anopheles mosquitoes',
    'long_description': None,
    'author': 'Sanjay Nagi',
    'author_email': 'sanjay.nagi@lstmed.ac.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
