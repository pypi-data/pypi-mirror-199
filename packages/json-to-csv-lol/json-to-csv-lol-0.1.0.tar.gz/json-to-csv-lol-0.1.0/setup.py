# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['json_to_csv_lol']

package_data = \
{'': ['*']}

install_requires = \
['polars>=0.16.16,<0.17.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['json-to-csv-lol = json_to_csv-lol.main:app']}

setup_kwargs = {
    'name': 'json-to-csv-lol',
    'version': '0.1.0',
    'description': '',
    'long_description': '# JSON to CSV Converter\n\nThis is a simple package for convert a JSON to a CSV File',
    'author': 'Eduardo Alvarez',
    'author_email': 'walojose46@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
