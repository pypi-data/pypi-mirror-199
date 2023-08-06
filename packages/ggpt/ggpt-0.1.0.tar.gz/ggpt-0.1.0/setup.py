# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ggpt']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'openai>=0.27.2,<0.28.0', 'rich>=13.3.2,<14.0.0']

entry_points = \
{'console_scripts': ['ggpt = ggpt.cli:cli']}

setup_kwargs = {
    'name': 'ggpt',
    'version': '0.1.0',
    'description': 'Gorgueous CLI tools using GPT',
    'long_description': '',
    'author': 'jenz0000',
    'author_email': 'fullswing0603@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
