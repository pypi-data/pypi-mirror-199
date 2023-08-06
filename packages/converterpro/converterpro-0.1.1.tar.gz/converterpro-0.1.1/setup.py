# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['converterpro']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'converterpro',
    'version': '0.1.1',
    'description': 'Python converter library',
    'long_description': '# ConverterPro\nA python library to convert units and currencies\n\n![Hex.pm](https://img.shields.io/hexpm/l/apa?style=flat&color=brightgreen)\n![GitHub issues](https://img.shields.io/github/issues/oforiwaasam/converterpro)\n[![Build Status](https://img.shields.io/github/actions/workflow/status/oforiwaasam/converterpro/build.yml)](https://github.com/oforiwaasam/converterpro/actions/workflows/build.yml)\n[![Coverage Status](https://coveralls.io/repos/github/oforiwaasam/converterpro/badge.svg?branch=main&kill_cache=1)](https://coveralls.io/github/oforiwaasam/converterpro?branch=main)\n[![black](https://img.shields.io/badge/code%20style-black-000000)](https://github.com/psf/black)\n[![poetry](https://img.shields.io/badge/packaging-poetry-008adf)](https://python-poetry.org/)\n\n## 🔭 Overview\nThis python library will allow developers to easily incorporate conversions into their programs without having to write all the logic for it. The library currently has the following functionalities:\n- Converting Metric System, Imperial System and US System Measurements\n\n## Installation\n\nInstall **converterpro** with `pip`:\n\n```bash\npip install converterpro\n```\n\n## 📝 Details\nThis library project is a pure python project using modern tooling. It uses a `Makefile` as a command registry, with the following commands:\n- `make`: list available commands\n- `make install`: install and build this library and its dependencies using `poetry`\n- `make lint`: perform static analysis of this library with `ruff` and `black`\n- `make format`: autoformat this library using `black` and `ruff`\n- `make test`: run automated tests with `pytest`\n- `make coverage`: run automated tests with `pytest` and collect coverage information\n\n## 👩🏾\u200d💻👨🏾\u200d Contributing\n\nPlease see [CONTRIBUTING](CONTRIBUTING.md) for more information.\n\n## License\n\nThis software is licensed under the Apache 2.0 license. Please see [LICENSE](LICENSE) for more information.\n\n## 🙎🏾\u200d Author\nMain Maintainer: Lily Sam\n\n',
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
