# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gptroles', 'gptroles.ui']

package_data = \
{'': ['*'], 'gptroles.ui': ['web/*', 'web/static/*']}

install_requires = \
['openai>=0.27.2',
 'pyqt6-webengine>=6.4.0',
 'pyqt6>=6.4.2',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['devtest = mypackage:test.run_tests',
                     'main = gptroles.main:main']}

setup_kwargs = {
    'name': 'gptroles',
    'version': '0.1.1',
    'description': 'Interact with chatgpt and assign different roles',
    'long_description': '\n# GPT Roles\nSimple PyQT chatbox that connects to a chat session with GPT.\n\nHas some features to increase interactivity and context awareness:\n    - GPT can request web pages or from APIs to answer your questions, to get current prices or latest news\n    - GPT can run shell scripts on your computer, so you can ask it directly to find files or open programs\n\nThese are programmed in a root prompt.\nBe direct as possible in your commands or questions to get them issued correctly.\n\nTODO: The chat UI has action indicators for the interactivity\nTODO: Also the messages in the current prompt chain are\n\nTODO: List and add roles from jailbreakchat.com\n\n## Installing/Running\n\n#### From source with Poetry\n```shell\npoetry install && poetry run main\n```\n\n#### From pip\nTODO\n\n',
    'author': 'Blipk A.D.',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/blipk/pysh',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
