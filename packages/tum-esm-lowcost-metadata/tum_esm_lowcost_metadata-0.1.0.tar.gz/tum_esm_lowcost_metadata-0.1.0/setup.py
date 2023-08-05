# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tum_esm_lowcost_metadata']

package_data = \
{'': ['*']}

modules = \
['py']
install_requires = \
['deepdiff>=6.3.0,<7.0.0',
 'pendulum>=2.1.2,<3.0.0',
 'pydantic>=1.10.4,<2.0.0',
 'tum-esm-utils>=1.2.1,<2.0.0']

setup_kwargs = {
    'name': 'tum-esm-lowcost-metadata',
    'version': '0.1.0',
    'description': "Single source of truth for ESM's lowcost measurement logistics",
    'long_description': '# Lowcost Metadata\n\nThis repository is the single source of truth for our lowcost measurement logistics: "Where has each station been on each day of measurements?" We selected this format over putting it in a database due to various reasons:\n\n-   Easy to read, modify and extend by selective group members using GitHub permissions\n-   Changes to this are more obvious here than in database logs\n-   Versioning (easy to revert mistakes)\n-   Automatic testing of the files integrities\n-   Easy import as a statically typed Python library\n\n<br/>\n\n## What does this data look like?\n\nThere is a set of locations in **`data/locations.json`**:\n\n```json\n[\n    {\n        "location_id": "TUM_I",\n        "details": "TUM Dach Innenstadt",\n        "lon": 11.569,\n        "lat": 48.151,\n        "alt": 539,\n        "colocations": [\n            { "colocation_type": "lfu", "colocation_station_id": "somestationid" },\n            { "colocation_type": "midcost", "colocation_station_id": "somestationid" },\n            { "colocation_type": "airquality", "colocation_station_id": "somestationid" }\n        ]\n    }\n]\n```\n\nThere is a set of sensors in **`data/sensors.json`** that measure at these location sites:\n\n```json\n[\n    {\n        "sensor_id": "tum_esm_lc_01",\n        "sensor_type": "DL-LP8",\n        "sensor_manufacturer": "Decentlab",\n        "details": "",\n        "serial_number": "someserialnumber",\n        "locations": [\n            {\n                "from_datetime": "2023-03-01T00:00:00+00:00",\n                "to_datetime": "2023-04-30T23:59:59+00:00",\n                "location_id": "TUM_LAB",\n                "mounting_orientation": 273,\n                "mounting_height": 3.25\n            }\n        ]\n    }\n]\n```\n\n<br/>\n\n## How to add new measurement days?\n\n1. Possibly add new locations in `data/locations.json`\n2. Extend the list of locations in `data/sensors.json`\n\n<br/>\n\n## How can I know whether my changes were correct?\n\nWhenever you make changes in the repository on GitHub, the integrity of the files will automatically be checked. You can check whether all tests have passed [here](https://github.com/tum-esm/lowcost-metadata/actions). If some have failed you can ask Moritz Makowski.\n\nA list of all integrity checks can be found in [`tests/README.md`](https://github.com/tum-esm/lowcost-metadata//tree/main/tests).\n\n<br/>\n\n## How to use it in your codebase?\n\n1. Install python library\n\n```bash\npoetry add tum_esm_lowcost_metadata\n# or\npip install tum_esm_lowcost_metadata\n```\n\n2. Create a personal access token for a GitHub account that has read access to the metadata repository: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token\n\n3. Use the metadata anywhere\n\n```python\nimport tum_esm_lowcost_metadata\n\nlowcost_metadata_interface = tum_esm_lowcost_metadata.load_from_github(\n    github_repository = "org-name/repo-name",\n    access_token = "ghp_..."\n)\n\nmetadata = lowcost_metadata_interface.get(\n    sensor_id = "tum_esm_lc_01", date = "20230301"\n)  # is of type list[tum_esm_lowcost_metadata.types.SensorDataContext]\n\nprint(metadata.dict())\n```\n\n... prints out:\n\n```json\n[\n    {\n        "sensor_id": "tum_esm_lc_01",\n        "sensor_type": "DL-LP8",\n        "sensor_manufacturer": "Decentlab",\n        "details": "",\n        "serial_number": "someserialnumber",\n        "from_datetime": "2023-03-01T00:00:00+00:00",\n        "to_datetime": "2023-04-30T23:59:59+00:00",\n        "mounting_orientation": "273",\n        "mounting_height": "3.25",\n        "location": {\n            "location_id": "TUM_LAB",\n            "details": "Inside the laboratory at TUM Innenstadt",\n            "lon": 11.569,\n            "lat": 48.151,\n            "alt": 521.0,\n            "colocations": []\n        }\n    }\n]\n```\n\n⚠️ The return type is a list because location records have time data.\nThe `get` method only accepts a date; hence there can be multiple\nlocations in one day.\n\n<br/>\n\n## For Developers: Publish the Package to PyPI\n\n```bash\npoetry build\npoetry publish\n```\n',
    'author': 'Moritz Makowski',
    'author_email': 'moritz.makowski@tum.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tum-esm/lowcost-metadata',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
