# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['maptiler', 'maptiler.cloud_cli']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['maptiler-cloud = maptiler.cloud_cli:cli']}

setup_kwargs = {
    'name': 'maptiler-cloud-cli',
    'version': '1.1.4',
    'description': 'CLI utility for MapTiler Cloud',
    'long_description': '# MapTiler Cloud CLI\nThis tool allows you [upload map data](https://documentation.maptiler.com/hc/en-us/articles/4408129705745-How-to-upload-MBTiles-or-GeoPackage-into-MapTiler-Cloud-using-API) into [MapTiler Cloud](https://www.maptiler.com/cloud/geodata-hosting/) using [upload API](https://docs.maptiler.com/cloud/admin-api/tileset_ingest/).\n\n## Requirements\n\n- Python *version >= 3.6*\n- pip\n- venv\n\n## Installation\n\n```shell\npip install maptiler-cloud-cli\n```\n\n## Authorization\n\nYou need an API token to be able to use the tool.\nThe token can be acquired from the\n[Credentials](https://cloud.maptiler.com/account/credentials/)\nsection of your account administration pages in MapTiler Cloud.\n\nSpecify it either on the command line or as an environment variable.\n\n```shell\nmaptiler-cloud --token=MY_TOKEN ...\n```\n\n```shell\nMAPTILER_TOKEN=MY_TOKEN; maptiler-cloud ...\n```\n\n## Usage\n\n### Create a new tileset\n\nTo create a new tileset, use the `tiles ingest` command.\n\n```shell\nmaptiler-cloud tiles ingest v1.mbtiles\n```\n\nThe command will print out the tileset ID on the last line.\n\n> :information_source: The GeoPackage must have a tile matrix set. Read the\n> [Vector tiles generating (basic)](https://documentation.maptiler.com/hc/en-us/articles/360020887038-Vector-tiles-generating-basic-)\n> article to learn how to create a valid GeoPackage or MBTiles from the\n> [MapTiler Engine application](https://www.maptiler.com/engine/).\n\n> :bulb: If you reach the tileset limit for your account, you will not be able to upload new tilesets, and you will get an error.\n> Check out our [plans](https://www.maptiler.com/cloud/plans/) to increase the number of tilesets you can have.\n\n### Update a tileset\n\nYou can use the tileset ID to upload a new file to the same tileset.\n\n```shell\nmaptiler-cloud tiles ingest --document-id=EXISTING_TILESET_ID v2.mbtiles\n```\n\n> :warning: This option **replaces** the tileset data with the data from the new file. It does **NOT** add the new data to the existing tileset.\n\nTo learn more about using this tool, read\n[How to upload MBTiles or GeoPackage into MapTiler Cloud](https://documentation.maptiler.com/hc/en-us/articles/4408129705745-How-to-upload-MBTiles-or-GeoPackage-into-MapTiler-Cloud-using-API).\n\nFor more control over tileset management, you can use the\n[Admin API](https://docs.maptiler.com/cloud/admin-api/).\nThe admin API allows you to create, update or delete a tileset among other actions.\n',
    'author': 'MapTiler',
    'author_email': 'info@maptiler.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/maptiler/maptiler-cloud-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
