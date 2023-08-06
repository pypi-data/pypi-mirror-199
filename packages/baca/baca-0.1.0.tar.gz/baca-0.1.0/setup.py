# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['baca',
 'baca.components',
 'baca.ebooks',
 'baca.resources',
 'baca.tools',
 'baca.tools.KindleUnpack',
 'baca.utils']

package_data = \
{'': ['*']}

install_requires = \
['appdirs>=1.4.4,<2.0.0',
 'beautifulsoup4>=4.12.0,<5.0.0',
 'fuzzywuzzy>=0.18.0,<0.19.0',
 'markdownify>=0.11.6,<0.12.0',
 'peewee>=3.16.0,<4.0.0',
 'textual>=0.16.0,<0.17.0']

entry_points = \
{'console_scripts': ['baca = baca.__main__:main']}

setup_kwargs = {
    'name': 'baca',
    'version': '0.1.0',
    'description': 'TUI Ebook Reader',
    'long_description': 'None',
    'author': 'Benawi Adha',
    'author_email': 'benawiadha@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
