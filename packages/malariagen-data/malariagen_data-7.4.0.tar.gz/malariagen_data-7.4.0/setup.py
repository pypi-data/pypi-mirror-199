# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['malariagen_data']

package_data = \
{'': ['*']}

install_requires = \
['BioPython',
 'bokeh<3.0',
 'dash',
 'dash-cytoscape',
 'dask[array]',
 'fsspec',
 'gcsfs',
 'igv-notebook>=0.2.3',
 'importlib_metadata<5.0',
 'ipinfo!=4.4.1',
 'ipyleaflet>0.17.0',
 'ipywidgets',
 'jupyter-dash',
 'numba',
 'numpydoc_decorator>=1.9.0',
 'plotly',
 'scikit-allel',
 'statsmodels',
 'tqdm',
 'typing_extensions',
 'xarray',
 'zarr']

extras_require = \
{':python_full_version >= "3.7.1" and python_version < "3.8"': ['numpy<1.22',
                                                                'scipy<1.8',
                                                                'pandas<1.4'],
 ':python_version >= "3.8"': ['numpy'],
 ':python_version >= "3.8" and python_version < "3.11"': ['scipy', 'pandas']}

setup_kwargs = {
    'name': 'malariagen-data',
    'version': '7.4.0',
    'description': 'A package for accessing and analysing MalariaGEN data.',
    'long_description': 'None',
    'author': 'Alistair Miles',
    'author_email': 'alistair.miles@sanger.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
