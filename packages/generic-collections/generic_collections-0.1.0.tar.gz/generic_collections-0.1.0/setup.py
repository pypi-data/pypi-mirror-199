# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['generic_collections',
 'generic_collections.enums',
 'generic_collections.objects']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.7,<2.0.0']

setup_kwargs = {
    'name': 'generic-collections',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'ventura94',
    'author_email': 'arianventura94@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
