# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gaffe']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'gaffe',
    'version': '0.1.1',
    'description': 'Simple structured exceptions for python.',
    'long_description': '# Gaffe\nSimple structured exceptions for python. \n\nGaffe relies on metaclass-based approach to be highly extensible and pluggable into any existing project, promoting better error handling and improved code readability.\n\n\n# Features\n\n- Simple and concise syntax for defining custom errors with optional subtypes\n- Clean integration through metaclass-based approach\n- Supports inheritance and composition of custom errors\n- Automatic generation of error classes with custom attributes\n- Easy comparison of errors using the __eq__ method, supporting both class and instance comparisons.\n\n# Installation\n\nWith pip:\n`pip install gaffe`\n\nor poetry:\n\n`poetry add gaffe`\n\n# Usage\n\nTo use this custom error system, simply import the Error class and define your custom errors by inheriting from it:\n\n```python\nfrom gaffe import Error\n\nclass NotFoundError(Exception):\n    ...\n\nclass MyError(Error):\n    not_found: NotFoundError\n    invalid_input: ...\n    authentication_error = "authentication_error"\n```\n\nThis creates three custom errors under the MyError class:\n- `MyError.not_found` which extends also `NotFoundError`\n- `MyError.invalid_input` the simplest definition of an error without additional subtype\n- `MyError.authentication_error` an error with a custom value assigned to it\n\nThese custom errors can be used just like any other Python exceptions:\n\n```python\nfrom gaffe import Error\n\nclass NotFoundError(Exception):\n    ...\n\nclass NetworkError(Error):\n    timeout = "Request timed out"\n    connection_error: ...\n\nclass HTTPError(NetworkError):\n    bad_request: ...\n    not_found: NotFoundError\n```\n\nThis creates a hierarchy of custom errors with NetworkError as the base class and HTTPError as a subclass with additional HTTP-specific errors.\n\nYou can handle `HTTPError.timeout` as follows:\n\n```python\ntry:\n    raise HTTPError.timeout\nexcept NetworkError as e:\n    print(e)\n\ntry:\n    raise HTTPError.timeout\nexcept HTTPError as e:\n    print(e)\n\ntry:\n    raise HTTPError.timeout\nexcept HTTPError.timeout as e:\n    print(e)\n```\n\nYou can handle `HTTPError.not_found` as follows:\n\n```python\ntry:\n    raise HTTPError.not_found\nexcept HTTPError as e:\n    print(e)\n\ntry:\n    raise HTTPError.not_found\nexcept HTTPError as e:\n    print(e)\n\ntry:\n    raise HTTPError.not_found\nexcept NotFoundError as e:\n    print(e)\n```\n\n# Integration with mypy\n\nTo fix mypy complains about the code you can use `gaffe.mypy:plugin` in your config file, like below:\n\n```toml\n[tool.mypy]\nplugins = "gaffe.mypy:plugin"\n```\n\nThat\'s all folks!\n\nFor more examples please [check the test scenarios](./tests/test_error.py).\n',
    'author': 'Dawid Kraczkowski',
    'author_email': 'dawid.kraczkowski@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kodemore/gaffe',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
