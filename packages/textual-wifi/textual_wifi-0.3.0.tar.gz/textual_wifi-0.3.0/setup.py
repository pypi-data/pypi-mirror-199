# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textual_wifi']

package_data = \
{'': ['*']}

install_requires = \
['nmcli>=1.1.2,<2.0.0', 'textual[dev]>=0.16.0,<0.17.0']

entry_points = \
{'console_scripts': ['textual_wifi = textual_wifi.main:main']}

setup_kwargs = {
    'name': 'textual-wifi',
    'version': '0.3.0',
    'description': 'A wifi application build with textual and nmcli (py)',
    'long_description': '',
    'author': 'Dmitrij Vinokour',
    'author_email': 'vinokour.dmitrij@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
