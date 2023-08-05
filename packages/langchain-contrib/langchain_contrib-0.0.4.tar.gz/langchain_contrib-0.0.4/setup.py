# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['langchain_contrib',
 'langchain_contrib.chains',
 'langchain_contrib.chains.mrkl',
 'langchain_contrib.llms',
 'langchain_contrib.llms.human',
 'langchain_contrib.prompts',
 'langchain_contrib.prompts.choice',
 'langchain_contrib.tools',
 'langchain_contrib.tools.terminal',
 'langchain_contrib.tools.terminal.patchers',
 'langchain_contrib.utils']

package_data = \
{'': ['*']}

install_requires = \
['fvalues>=0.0.3,<0.0.4',
 'langchain>=0.0.119,<0.0.120',
 'pexpect>=4.8.0,<5.0.0',
 'simple-term-menu>=1.6.1,<2.0.0']

setup_kwargs = {
    'name': 'langchain-contrib',
    'version': '0.0.4',
    'description': '',
    'long_description': '# langchain-contrib\n\nA collection of utilities that are too experimental for [langchain proper](https://github.com/hwchase17/langchain), but are nonetheless generic enough to potentially be useful for multiple projects. Currently consists of code dumped from [ZAMM](https://github.com/amosjyng/zamm), but is of course open to contributions with lax procedures.\n\n## Quickstart\n\n```bash\npip install langchain-contrib\n```\n\nTo add interop with [`vcr-langchain`](https://github.com/amosjyng/vcr-langchain), simply install it as well:\n\n```bash\npip install vcr-langchain\n```\n',
    'author': 'Amos Jun-yeung Ng',
    'author_email': 'me@amos.ng',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
