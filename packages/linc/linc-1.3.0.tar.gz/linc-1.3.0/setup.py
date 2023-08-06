# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['linc', 'linc.config', 'linc.parse', 'linc.write']

package_data = \
{'': ['*']}

install_requires = \
['netCDF4>=1.6.2,<2.0.0',
 'numpy>=1.23.4,<2.0.0',
 'pydantic>=1.10.2,<2.0.0',
 'tomli>=2.0.1,<3.0.0',
 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['linc = linc.cli:app']}

setup_kwargs = {
    'name': 'linc',
    'version': '1.3.0',
    'description': 'A package to handle LICEL Binary format',
    'long_description': '# Linc\n---\nLinc is a fast way to convert [Licel Raw Format](https://licel.com/raw_data_format.html) into netCDF4 to handle data easier.\n',
    'author': 'Juan Diego',
    'author_email': 'jdlar@eafit.edu.co',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
