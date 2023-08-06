# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['embedding_explorer',
 'embedding_explorer.blueprints',
 'embedding_explorer.components',
 'embedding_explorer.plots',
 'embedding_explorer.prepare']

package_data = \
{'': ['*'], 'embedding_explorer': ['assets/*']}

install_requires = \
['dash-extensions>=0.1.10,<0.2.0',
 'dash-iconify>=0.1.2,<0.2.0',
 'dash-mantine-components>=0.11.1,<0.12.0',
 'dash>=2.7.1,<2.8.0',
 'joblib>=1.2.0,<1.3.0',
 'levenshtein>=0.20.9,<0.21.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.2,<1.6.0',
 'scikit-learn>=1.2.0,<1.3.0',
 'thefuzz>=0.19.0,<0.20.0',
 'wordcloud>=1.8.2.2,<1.9.0.0']

setup_kwargs = {
    'name': 'embedding-explorer',
    'version': '0.1.1',
    'description': 'Tools for interactive visual inspection of static word embedding models.',
    'long_description': '# embedding-explorer\nTools for interactive visual exploration of static word embedding models.\n',
    'author': 'Márton Kardos',
    'author_email': 'power.up1163@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0',
}


setup(**setup_kwargs)
