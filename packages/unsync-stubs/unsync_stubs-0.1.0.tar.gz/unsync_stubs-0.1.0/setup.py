# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unsync-stubs']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'unsync-stubs',
    'version': '0.1.0',
    'description': '',
    'long_description': '# unsync-stubs\nThis package contains type stubs for https://github.com/alex-sherman/unsync package\n',
    'author': 'Niraj',
    'author_email': 'niraj@polywrap.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
