# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['databricks_sdk_python']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.4.0,<2.0.0', 'requests>=2.22']

setup_kwargs = {
    'name': 'databricks-sdk-python',
    'version': '0.0.0',
    'description': 'Objet based databricks sdk',
    'long_description': '# databricks-sdk-python',
    'author': "Peter van 't Hof'",
    'author_email': 'peter.vanthof@godatadriven.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ffinfo/databricks-sdk-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0',
}


setup(**setup_kwargs)
