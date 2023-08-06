# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sphinx_tfdoc']

package_data = \
{'': ['*'], 'sphinx_tfdoc': ['templates/*']}

install_requires = \
['Jinja2', 'sphinx', 'tabulate']

setup_kwargs = {
    'name': 'sphinx-tfdoc',
    'version': '0.1.0',
    'description': 'Sphinx API documentation for Terraform Modules',
    'long_description': 'None',
    'author': 'Tommy Wang',
    'author_email': 'twang@august8.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/twang817/sphinx-tfdoc',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
