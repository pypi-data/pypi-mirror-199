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
    'version': '0.1.1',
    'description': 'Gorgeous CLI tools using GPT',
    'long_description': '# ggpt\n\n##### Gorgeous CLI tools using GPT.\n\n<br/>\n<br/>\n\n## Installation\n\n\n```\npip install ggpt\n```\n\n<br/>\n<br/>\n\n## Setup\n1. Obtain an OpenAI API key at https://beta.openai.com/account/api-keys\n\n2. Add it to your shell environment variables\n\t```\n\texport OPENAI_API_KEY=<YOUR_API_KEY_HERE>\n\t```\n\n<br/>\n<br/>\n\n## Usage\n\n<br/>\n\n###  docstring\n\n###### generates automated docstring based on code changes.\n\n\n<br/> \n\n```\nggpt docstring [OPTIONS]\n```\n\n<br/>\n\n| Option         | Description                                       |\n| -------------- | ------------------------------------------------- |\n| `--api-key TEXT`|OpenAI API Key. <br/> If not provided, `OPENAI_API_KEY` environment variable is used. |\n| `--path PATH`   | Path to the Git repository to search for code changes. <br/> If not provided, the current directory is used.|\n| `--hash TEXT`   | Hash of the commit to review. <br/>  If not provided, unstaged changes are reviewed by default.     |\n| `--staged`      | Include only staged changes in the review. <br/> If not provided, unstaged changes are reviewed by default.  |\n\n<br/>\n\nhttps://user-images.githubusercontent.com/123562684/227761450-9297f709-3d61-448c-ad78-a04f9a5f41d8.mov\n\n<br/>\n\n---\n\n<br/>\n\n\n###  review\n\n###### generates automated code review based on code changes.\n\n\n<br/>\n\n```\nggpt review [OPTIONS]\n```\n\n<br/>\n\n| Option         | Description                                       |\n| -------------- | ------------------------------------------------- |\n| `--api-key TEXT`|OpenAI API Key. <br/> If not provided, `OPENAI_API_KEY` environment variable is used. |\n| `--path PATH`   | Path to the Git repository to search for code changes. <br/> If not provided, the current directory is used.|\n| `--hash TEXT`   | Hash of the commit to review. <br/>  If not provided, unstaged changes are reviewed by default.     |\n| `--staged`      | Include only staged changes in the review. <br/> If not provided, unstaged changes are reviewed by default.  |\n\n<br/>\n\nhttps://user-images.githubusercontent.com/123562684/227762097-1c42b186-014f-48fe-b116-ee5e6c39f9f7.mov\n\n<br/>\n\n---\n\n<br/>\n\n\n###  naming\n\n###### suggests variable names based on submitted prompt. \n\n\n<br/>\n\n```\nggpt naming PROMPT [OPTIONS]\n```\n\n<br/>\n\n| Option         | Description                                       |\n| -------------- | ------------------------------------------------- |\n| `--api-key TEXT`|OpenAI API Key. <br/> If not provided, `OPENAI_API_KEY` environment variable is used. |\n\n<br/>\n\nhttps://user-images.githubusercontent.com/123562684/227763626-d329f156-c7f6-4a46-bfee-57504882d62c.mov\n\n\n<br/>\n\n## License\n\n\nMIT LISENCE',
    'author': 'jenz0000',
    'author_email': 'fullswing0603@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jenz0000/ggpt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
