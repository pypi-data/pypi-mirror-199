# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['match_srt']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'opencv-python>=4.7.0,<5.0.0',
 'pysrt>=1.1.2,<2.0.0',
 'rich>=13.3.3,<14.0.0']

entry_points = \
{'console_scripts': ['match_srt = match_srt.match_srt:matching']}

setup_kwargs = {
    'name': 'match-srt',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'MasterGowen',
    'author_email': 'mastergowen@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/urfu-online/match_srt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
