# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastapi_cli_tool',
 'fastapi_cli_tool.templates',
 'fastapi_cli_tool.templates.app',
 'fastapi_cli_tool.templates.app.hooks',
 'fastapi_cli_tool.templates.app.{{ cookiecutter.folder_name }}',
 'fastapi_cli_tool.templates.app.{{ cookiecutter.folder_name }}.api',
 'fastapi_cli_tool.templates.app.{{ cookiecutter.folder_name }}.crud',
 'fastapi_cli_tool.templates.project',
 'fastapi_cli_tool.templates.project.hooks',
 'fastapi_cli_tool.templates.project.{{ cookiecutter.folder_name }}',
 'fastapi_cli_tool.templates.project.{{ cookiecutter.folder_name }}.backend',
 'fastapi_cli_tool.templates.project.{{ cookiecutter.folder_name }}.core',
 'fastapi_cli_tool.templates.project.{{ cookiecutter.folder_name }}.core.conf',
 'fastapi_cli_tool.templates.project.{{ cookiecutter.folder_name '
 '}}.core.contrib',
 'fastapi_cli_tool.templates.project.{{ cookiecutter.folder_name }}.core.utils',
 'fastapi_cli_tool.templates.project.{{ cookiecutter.folder_name }}.tests']

package_data = \
{'': ['*']}

install_requires = \
['cookiecutter>=2.1.1,<3.0.0',
 'pydantic[email]>=1.10.5,<2.0.0',
 'questionary>=1.10.0,<2.0.0',
 'requests>=2.28.2,<3.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['fastapi-cli = fastapi_cli_tool.main:app']}

setup_kwargs = {
    'name': 'fastapi-cli-tool',
    'version': '0.1.3',
    'description': 'A CLI Tool to Create and Manage FastAPI Apps',
    'long_description': '',
    'author': 'Christoph-xd',
    'author_email': 'cbsk.tech@gmail.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
