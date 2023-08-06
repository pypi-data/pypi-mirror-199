# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['padmy', 'padmy.anonymize', 'padmy.migration', 'padmy.sampling']

package_data = \
{'': ['*']}

install_requires = \
['Faker>=13.15.1,<14.0.0',
 'PyYAML>=6.0,<7.0',
 'asyncpg>=0.27.0,<0.28.0',
 'piou>=0.13.1,<0.14.0',
 'typing-extensions>=4.3.0,<5.0.0']

extras_require = \
{'network': ['networkx>=2.8.5,<3.0.0',
             'dash>=2.6.0,<3.0.0',
             'dash-cytoscape>=0.3.0,<0.4.0']}

entry_points = \
{'console_scripts': ['cli = run:run']}

setup_kwargs = {
    'name': 'padmy',
    'version': '0.4.0',
    'description': '',
    'long_description': 'None',
    'author': 'andarius',
    'author_email': 'julien.brayere@tracktor.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
