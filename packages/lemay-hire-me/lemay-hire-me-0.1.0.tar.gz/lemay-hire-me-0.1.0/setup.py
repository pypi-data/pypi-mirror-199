# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lemay_hire_me',
 'lemay_hire_me.schemas',
 'lemay_hire_me.utils',
 'lemay_hire_me.utils.config',
 'lemay_hire_me.utils.db',
 'lemay_hire_me.validators']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.31,<4.0.0',
 'PyInquirer>=1.0.3,<2.0.0',
 'pydantic>=1.10.5,<2.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'requests>=2.28.2,<3.0.0',
 'termcolor>=2.2.0,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['lemay-hire-me = lemay_hire_me.main:app']}

setup_kwargs = {
    'name': 'lemay-hire-me',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Alexey Belochenko',
    'author_email': 'alexey@lemay.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
