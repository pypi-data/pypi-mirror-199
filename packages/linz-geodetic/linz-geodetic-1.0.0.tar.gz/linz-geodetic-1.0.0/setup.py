# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['LINZ', 'LINZ.Geodetic']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.21,<2.0']

setup_kwargs = {
    'name': 'linz-geodetic',
    'version': '1.0.0',
    'description': 'LINZ.geodetic module - miscellanous geodetic functions',
    'long_description': '# LINZ.geodetic package\n\nSome random geodetic functions used by other LINZ modules.  \n\n* Ellipsoid.py: Conversion between ellipsoidal and geocentric coordinates.  Also [GRS80](https://en.wikipedia.org/wiki/Geodetic_Reference_System_1980) ellipsoid definition.\n* ITRF.py: Conversion between [ITRF](https://itrf.ign.fr/en/homepage) realisations\n* Sinex.py: Reading and some updating of [SINEX](https://www.iers.org/IERS/EN/Organization/AnalysisCoordinator/SinexFormat/sinex.html) files (GNSS processing solution files)\n',
    'author': 'Chris Crook',
    'author_email': 'ccrook@linz.govt.nz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/linz/python-linz-geodetic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
