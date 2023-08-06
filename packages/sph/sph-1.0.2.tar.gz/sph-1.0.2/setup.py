# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sph']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.27,<4.0.0',
 'PyYAML==5.4.1',
 'aiohttp>=3.8.4,<4.0.0',
 'click>=8.1.3,<9.0.0',
 'colorama>=0.4.4,<0.5.0',
 'halo>=0.0.31,<0.0.32',
 'python-dateutil>=2.8.2,<3.0.0',
 'setuptools>=62.1.0,<63.0.0',
 'witchtui==0.1.3',
 'xdg>=5.1.1,<6.0.0']

entry_points = \
{'console_scripts': ['sph = sph.sph:be_helpful',
                     'workflow = sph.workflow:be_helpful']}

setup_kwargs = {
    'name': 'sph',
    'version': '1.0.2',
    'description': '',
    'long_description': 'None',
    'author': 'François Poizat',
    'author_email': 'francois.poizat@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
