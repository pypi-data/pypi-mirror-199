# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['representty']
install_requires = \
['ipython', 'rich>=13.3.1,<14.0.0']

entry_points = \
{'console_scripts': ['rtty = representty:just_call_the_script']}

setup_kwargs = {
    'name': 'representty',
    'version': '0.1.1',
    'description': 'Tiny presentation tool based on rich and markdown',
    'long_description': None,
    'author': 'L3viathan',
    'author_email': 'git@l3vi.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
