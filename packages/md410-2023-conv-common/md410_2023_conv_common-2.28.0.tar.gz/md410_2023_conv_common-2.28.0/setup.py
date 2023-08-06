# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['md410_2023_conv_common']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.20.3,<2.0.0',
 'click>=8.0.3,<9.0.0',
 'docker>=5.0.3,<6.0.0',
 'filetype>=1.2.0,<2.0.0',
 'pydantic>=1.8.2,<2.0.0',
 'python-dotenv>=0.19.2,<0.20.0',
 'redmail>=0.2.0,<0.3.0',
 'rich>=13.0.0,<14.0.0',
 'sendgrid>=6.9.7,<7.0.0']

setup_kwargs = {
    'name': 'md410-2023-conv-common',
    'version': '2.28.0',
    'description': 'Common libraries for applications related to the 2023 Lions MD410 Convention',
    'long_description': '# Introduction\n\nCommon libraries for applications related to the 2023 Lions Multiple District 410 Convention.\n\n# Associated Applications\n\nSee [this Gitlab group](https://gitlab.com/md410-2023-convention) for associated applications.\n',
    'author': 'Kim van Wyk',
    'author_email': 'vanwykk@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/md410_2023_conv/md410_2023_conv_common',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
