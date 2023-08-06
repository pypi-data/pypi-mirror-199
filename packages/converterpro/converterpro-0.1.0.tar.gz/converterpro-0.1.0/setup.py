# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['converterpro']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'converterpro',
    'version': '0.1.0',
    'description': 'Python converter library',
    'long_description': '# Converter\nA python library to convert units and currencies\n\n![Hex.pm](https://img.shields.io/hexpm/l/apa?style=flat&color=brightgreen)\n![GitHub issues](https://img.shields.io/github/issues/oforiwaasam/converter)\n\n## 🔭 Overview\nThis python library will allow developers to easily incorporate conversions into their programs without having to write all the logic for it.\n',
    'author': 'Lily Sam',
    'author_email': 'los2119@columbia.edu',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
