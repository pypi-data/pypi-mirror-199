# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['celery_yandex_serverless']

package_data = \
{'': ['*']}

install_requires = \
['celery>=5,<6', 'django>=4,<5']

setup_kwargs = {
    'name': 'celery-yandex-serverless',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'atnartur',
    'author_email': 'i@atnartur.ru',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
