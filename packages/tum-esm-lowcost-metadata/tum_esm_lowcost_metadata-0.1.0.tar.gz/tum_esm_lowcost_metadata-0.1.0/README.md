# Lowcost Metadata

This repository is the single source of truth for our lowcost measurement logistics: "Where has each station been on each day of measurements?" We selected this format over putting it in a database due to various reasons:

-   Easy to read, modify and extend by selective group members using GitHub permissions
-   Changes to this are more obvious here than in database logs
-   Versioning (easy to revert mistakes)
-   Automatic testing of the files integrities
-   Easy import as a statically typed Python library

<br/>

## What does this data look like?

There is a set of locations in **`data/locations.json`**:

```json
[
    {
        "location_id": "TUM_I",
        "details": "TUM Dach Innenstadt",
        "lon": 11.569,
        "lat": 48.151,
        "alt": 539,
        "colocations": [
            { "colocation_type": "lfu", "colocation_station_id": "somestationid" },
            { "colocation_type": "midcost", "colocation_station_id": "somestationid" },
            { "colocation_type": "airquality", "colocation_station_id": "somestationid" }
        ]
    }
]
```

There is a set of sensors in **`data/sensors.json`** that measure at these location sites:

```json
[
    {
        "sensor_id": "tum_esm_lc_01",
        "sensor_type": "DL-LP8",
        "sensor_manufacturer": "Decentlab",
        "details": "",
        "serial_number": "someserialnumber",
        "locations": [
            {
                "from_datetime": "2023-03-01T00:00:00+00:00",
                "to_datetime": "2023-04-30T23:59:59+00:00",
                "location_id": "TUM_LAB",
                "mounting_orientation": 273,
                "mounting_height": 3.25
            }
        ]
    }
]
```

<br/>

## How to add new measurement days?

1. Possibly add new locations in `data/locations.json`
2. Extend the list of locations in `data/sensors.json`

<br/>

## How can I know whether my changes were correct?

Whenever you make changes in the repository on GitHub, the integrity of the files will automatically be checked. You can check whether all tests have passed [here](https://github.com/tum-esm/lowcost-metadata/actions). If some have failed you can ask Moritz Makowski.

A list of all integrity checks can be found in [`tests/README.md`](https://github.com/tum-esm/lowcost-metadata//tree/main/tests).

<br/>

## How to use it in your codebase?

1. Install python library

```bash
poetry add tum_esm_lowcost_metadata
# or
pip install tum_esm_lowcost_metadata
```

2. Create a personal access token for a GitHub account that has read access to the metadata repository: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token

3. Use the metadata anywhere

```python
import tum_esm_lowcost_metadata

lowcost_metadata_interface = tum_esm_lowcost_metadata.load_from_github(
    github_repository = "org-name/repo-name",
    access_token = "ghp_..."
)

metadata = lowcost_metadata_interface.get(
    sensor_id = "tum_esm_lc_01", date = "20230301"
)  # is of type list[tum_esm_lowcost_metadata.types.SensorDataContext]

print(metadata.dict())
```

... prints out:

```json
[
    {
        "sensor_id": "tum_esm_lc_01",
        "sensor_type": "DL-LP8",
        "sensor_manufacturer": "Decentlab",
        "details": "",
        "serial_number": "someserialnumber",
        "from_datetime": "2023-03-01T00:00:00+00:00",
        "to_datetime": "2023-04-30T23:59:59+00:00",
        "mounting_orientation": "273",
        "mounting_height": "3.25",
        "location": {
            "location_id": "TUM_LAB",
            "details": "Inside the laboratory at TUM Innenstadt",
            "lon": 11.569,
            "lat": 48.151,
            "alt": 521.0,
            "colocations": []
        }
    }
]
```

⚠️ The return type is a list because location records have time data.
The `get` method only accepts a date; hence there can be multiple
locations in one day.

<br/>

## For Developers: Publish the Package to PyPI

```bash
poetry build
poetry publish
```
