# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clouds', 'clouds.aws']

package_data = \
{'': ['*']}

install_requires = \
['boto3', 'click', 'colorlog']

setup_kwargs = {
    'name': 'redhat-qe-cloud-tools',
    'version': '1.0.0',
    'description': 'Python utilities to manage cloud services, such as AWS.',
    'long_description': '# cloud-tools\nPython utilities to manage cloud services, such as AWS.\n\n## Local run\n\nclone the [repository](https://github.com/RedHatQE/cloud-tools.git)\n\n```\ngit clone https://github.com/RedHatQE/cloud-tools.git\n```\n\nInstall [poetry](https://github.com/python-poetry/poetry)\n\n```\npoetry install\n```\n\n## Docs\n- [AWS readme](aws/README.md)\n',
    'author': 'Meni Yakove',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/RedHatQE/cloud-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
