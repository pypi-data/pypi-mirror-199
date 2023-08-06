# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['freak']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'freak',
    'version': '0.0.0',
    'description': 'Real-time experiments control',
    'long_description': '# Freak\n\nFreak - real-time experiments control.\n\n',
    'author': 'Daniel Gafni',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
