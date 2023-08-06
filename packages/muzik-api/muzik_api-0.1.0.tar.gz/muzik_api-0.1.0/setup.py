# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['muzik_api']

package_data = \
{'': ['*']}

install_requires = \
['Django>=4.1.7,<5.0.0',
 'django-filter>=23.1,<24.0',
 'djangorestframework>=3.14.0,<4.0.0',
 'markdown>=3.4.3,<4.0.0']

setup_kwargs = {
    'name': 'muzik-api',
    'version': '0.1.0',
    'description': 'Free Personal Music API',
    'long_description': '# Music API\n\nPersonal Music API to download and search music from several platforms such as JioSaavn. ',
    'author': 'Dhrumil Mistry',
    'author_email': '56185972+dmdhrumilmistry@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
