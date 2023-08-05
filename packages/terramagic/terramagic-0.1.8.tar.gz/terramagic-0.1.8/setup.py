# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['terramagic']
install_requires = \
['click>=8.0.3,<9.0.0', 'python-hcl2>=4.3.0,<5.0.0', 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['terramagic = terramagic:main']}

setup_kwargs = {
    'name': 'terramagic',
    'version': '0.1.8',
    'description': 'A automate tool for terraform projects',
    'long_description': '# Terramagic CLI\n\n## Motivation\n\nEvery time , I needed create a terraform files to a new project, and a new terraform files., but this is not good. and now we have a Terramagic tool to help us to create a terraform files.\n\n## Requirements\n\n- Python 3.8 >=\n\n## How to install?\n\n```shell\npip install terramagic\n```\n\n## Check the version\n\n```bash\nterramagic --version\n```\n\n### Create a new project\n\n```shell\nterramagic create --name <project name> --env <env>\n```\n\n```shell\nterramagic create --name terraform --env prod --env dev\n```\n\n### Delete a project\n\n```shell\nterramagic delete --name <project name>\n```\n\n### Check if all terraform files configuration are valid.\n\n```shell\nterramagic check --name <project name>\n```\n\n## How to use this tool ?\n\n```shell\nUsage: terramagic [OPTIONS] COMMAND [ARGS]...\n\n  ClI tool to create Terraform project\n\nOptions:\n  -v, --version  Show version\n  --help         Show this message and exit.\n\nCommands:\n  check   Check all files inside a Terraform project are valid.\n  create  Create a new Terraform project with specified name and environment\n  remove  Delete the project\n```\n\nEnjoy!\n',
    'author': 'Milton Jesus',
    'author_email': 'milton.lima@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/miltlima/terramagic',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
