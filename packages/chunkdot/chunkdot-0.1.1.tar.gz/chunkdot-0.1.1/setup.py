# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chunkdot']

package_data = \
{'': ['*']}

install_requires = \
['numba>=0.56.4,<0.57.0', 'numpy>=1.23,<2.0', 'scipy>=1.10.1,<2.0.0']

setup_kwargs = {
    'name': 'chunkdot',
    'version': '0.1.1',
    'description': 'Multi-threaded matrix multiplication and cosine similarity calculations.',
    'long_description': '# ChunkDot\n\nMulti-threaded matrix multiplication and cosine similarity calculations. Appropriate for the calculation of the K most similar items for a large number of items (~1 Million) by partitioning the item matrix representation (embeddings) and using Numba to accelerate the calculations.\n',
    'author': 'Rodrigo Agundez',
    'author_email': 'rragundez@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.12',
}


setup(**setup_kwargs)
