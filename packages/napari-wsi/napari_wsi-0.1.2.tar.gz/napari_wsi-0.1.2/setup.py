# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['napari_wsi']

package_data = \
{'': ['*']}

install_requires = \
['dask>=2022',
 'imagecodecs>=2022',
 'magicgui<1.0.0',
 'matplotlib>=3.0.0,<4.0.0',
 'napari>=0.4.0,<0.5.0',
 'numpy>=1.0.0,<2.0.0',
 'pydantic!=1.10.0',
 'rasterio>=1.0.0,<2.0.0',
 'tifffile>=2022',
 'zarr>=2.0.0,<3.0.0']

entry_points = \
{'napari.manifest': ['napari-wsi = napari_wsi:napari.yaml']}

setup_kwargs = {
    'name': 'napari-wsi',
    'version': '0.1.2',
    'description': 'A plugin to read whole slide images within napari.',
    'long_description': '# napari-wsi\n\n[![PyPI](https://img.shields.io/pypi/v/napari-wsi.svg?color=green)](https://pypi.org/project/napari-wsi)\n[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-wsi)](https://napari-hub.org/plugins/napari-wsi)\n[![Tests](https://github.com/AstraZeneca/napari-wsi/actions/workflows/main.yml/badge.svg)](https://github.com/AstraZeneca/napari-wsi/actions)\n![Maturity Level-1](https://img.shields.io/badge/Maturity%20Level-ML--1-yellow)\n\nA plugin to read whole slide images within [napari].\n\n---\n\n## Installation\n\nYou can install `napari-wsi` via [pip]:\n\n```bash\npip install napari-wsi\n```\n\nTo install the latest development version, run:\n```bash\npip install git+https://github.com/AstraZeneca/napari-wsi.git\n```\n\n# Description\n\nThis [napari] plugin provides a reader for various whole slide image formats.\n\nBy default, any of the following formats is read using the [tifffile] library.\nIf the image file contains a tag `GDAL_METADATA`, the [rasterio] library is used\ninstead.\n\n- .bif\n- .ndpi\n- .qptiff\n- .scn\n- .svs\n- .tif\n- .tiff\n\n# Quickstart\n\nFrom the terminal:\n\n```bash\nnapari CMU-1.svs\n```\n\nFrom python:\n\n```python\nimport napari\n\nviewer = napari.Viewer()\nviewer.open("CMU-1.svs")\n```\n\n[napari]: https://github.com/napari/napari\n[pip]: https://pypi.org/project/pip/\n[rasterio]: https://github.com/rasterio/rasterio\n[tifffile]: https://github.com/cgohlke/tifffile\n',
    'author': 'Philipp Plewa',
    'author_email': 'philipp.plewa@astrazeneca.com',
    'maintainer': 'Philipp Plewa',
    'maintainer_email': 'philipp.plewa@astrazeneca.com',
    'url': 'https://github.com/AstraZeneca/napari-wsi',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
