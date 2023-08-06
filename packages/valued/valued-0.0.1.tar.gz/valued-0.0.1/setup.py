# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['valued']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'valued',
    'version': '0.0.1',
    'description': '',
    'long_description': '# Valued Python Client\n\nA Python client library for sending events to [Valued](https://valued.app).\n',
    'author': 'Support',
    'author_email': 'hello@valued.app',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
