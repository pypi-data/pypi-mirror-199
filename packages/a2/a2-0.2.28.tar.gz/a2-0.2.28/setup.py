# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['a2',
 'a2.cli',
 'a2.cli.cli_plotting',
 'a2.data',
 'a2.data.emoji',
 'a2.data.vocabularies',
 'a2.dataset',
 'a2.plotting',
 'a2.preprocess',
 'a2.training',
 'a2.twitter',
 'a2.utils']

package_data = \
{'': ['*']}

install_requires = \
['DateTime>=4.4,<5.0',
 'Shapely>=1.8.2,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'convertbng>=0.6.39,<0.7.0',
 'dask>=2022.6.1,<2023.0.0',
 'emoji<1.0.0',
 'geopy>=2.3.0,<3.0.0',
 'h5netcdf>=1.0.1,<2.0.0',
 'h5py>=3.7.0,<4.0.0',
 'ipython>=8.7.0,<9.0.0',
 'ipywidgets>=7.7.1,<8.0.0',
 'jsonlines>=3.1.0,<4.0.0',
 'jupyterlab>=3.4.3,<4.0.0',
 'kaleido==0.2.1',
 'mantik>=0.1.0,<0.2.0',
 'matplotlib>=3.5.2,<4.0.0',
 'netCDF4>=1.6.0,<2.0.0',
 'pandas>=1.4.2,<2.0.0',
 'plotly>=5.11.0,<6.0.0',
 'pyproj>=3.3.1,<4.0.0',
 'pytest-recording>=0.12.1,<0.13.0',
 'pytest-xdist>=2.5.0,<3.0.0',
 'rasterio>=1.3.3,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'rioxarray>=0.12.2,<0.13.0',
 'scikit-learn>=1.1.2,<2.0.0',
 'seaborn>=0.12.1,<0.13.0',
 'spacymoji>=3.0.1,<4.0.0',
 'tweepy>=4.10.0,<5.0.0',
 'urllib3>=1.26.12,<2.0.0',
 'wget>=3.2,<4.0',
 'wordcloud>=1.8.2,<2.0.0',
 'xarray>=2022.3.0,<2023.0.0']

entry_points = \
{'console_scripts': ['a2 = a2.cli.main:cli']}

setup_kwargs = {
    'name': 'a2',
    'version': '0.2.28',
    'description': 'Package for predicting information about the weather from social media data as application 2 for maelstrom project',
    'long_description': 'None',
    'author': 'Kristian Ehlert',
    'author_email': 'kristian.ehlert@4-cast.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)
