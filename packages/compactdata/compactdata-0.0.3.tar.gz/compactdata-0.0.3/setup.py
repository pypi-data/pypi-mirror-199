# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['compactdata']

package_data = \
{'': ['*']}

install_requires = \
['ply>=3.11,<4.0']

setup_kwargs = {
    'name': 'compactdata',
    'version': '0.0.3',
    'description': 'Python package for CompactData encoding and decoding',
    'long_description': '# CompactData\n\nThis is a placeholder package for a CompactData python parser.',
    'author': 'NUM Technology',
    'author_email': 'developer@num.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://compactdata.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
