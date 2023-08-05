from datetime import datetime, timedelta
import json
from typing import Any, Callable, Optional
from pydantic import BaseModel
import tum_esm_utils
from tum_esm_lowcost_metadata import types
import pendulum


class LowcostMetadataInterface:
    def __init__(
        self,
        locations: list[types.Location],
        sensors: list[types.Sensor],
    ):
        self.locations = locations
        self.sensors = sensors

        self.location_ids = [s.location_id for s in self.locations]
        self.sensor_ids = [s.sensor_id for s in self.sensors]

        _test_data_integrity(self.locations, self.sensors)

    def get(self, sensor_id: str, date_string: str) -> list[types.SensorDataContext]:
        """
        For a given `sensor_id` and `date_string`, return the metadata. The date is in
        the format of `YYYYMMDD` or `YYYY-MM-DD` (both UTC time).

        Returns the `pydantic` type `tum_esm_em27_metadata.types.SensorDataContext`:

        ```python
        from pydantic import BaseModel

        class LocationColocation(BaseModel):
            colocation_type: str
            colocation_station_id: str

        class Location(BaseModel):
            location_id: str
            details: str
            lon: float
            lat: float
            alt: float
            colocations: list[LocationColocation]

        class SensorDataContext(BaseModel):
            sensor_id: str
            sensor_type: str
            sensor_manufacturer: str
            details: str
            serial_number: str
            from_datetime: pendulum.DateTime
            to_datetime: pendulum.DateTime
            mounting_orientation: str
            mounting_height: str
            location: Location
        ```
        """

        # get the sensor
        assert sensor_id in self.sensor_ids, f'No location data for sensor_id "{sensor_id}"'
        sensor = list(filter(lambda s: s.sensor_id == sensor_id, self.sensors))[0]

        # convert any date to `YYYY-MM-DD`
        if len(date_string) == 8:
            date_string = f"{date_string[:4]}-{date_string[4:6]}-{date_string[6:]}"

        morning_datetime = pendulum.from_format(
            date_string + "T00:00:00+00:00", "YYYY-MM-DDTHH:mm:ssZ"
        )
        evening_datetime = pendulum.from_format(
            date_string + "T23:59:59+00:00", "YYYY-MM-DDTHH:mm:ssZ"
        )

        # in sensor.locations find the location that is active on the date
        location_matches = list(
            filter(
                lambda l: (
                    (l.from_datetime <= morning_datetime <= l.to_datetime)
                    or (l.from_datetime <= evening_datetime <= l.to_datetime)
                ),
                sensor.locations,
            )
        )

        assert (
            len(location_matches) > 0
        ), f"no location data for {sensor_id}/{date_string.replace('-', '')}"

        # bundle the context
        results = [
            types.SensorDataContext(
                sensor_id=sensor_id,
                sensor_type=sensor.sensor_type,
                sensor_manufacturer=sensor.sensor_manufacturer,
                details=sensor.details,
                serial_number=sensor.serial_number,
                from_datetime=m.from_datetime,
                to_datetime=m.to_datetime,
                mounting_orientation=m.mounting_orientation,
                mounting_height=m.mounting_height,
                location=list(filter(lambda l: l.location_id == m.location_id, self.locations))[0],
            )
            for m in location_matches
        ]

        if results[-1].to_datetime > evening_datetime:
            results[-1].to_datetime = evening_datetime
        if results[0].from_datetime < morning_datetime:
            results[0].from_datetime = morning_datetime

        return results


def load_from_github(
    github_repository: str,
    access_token: Optional[str] = None,
) -> LowcostMetadataInterface:
    """loads an EM27MetadataInterface from GitHub"""

    _req: Callable[[str], list[Any]] = lambda t: json.loads(
        tum_esm_utils.github.request_github_file(
            github_repository=github_repository,
            filepath=f"data/{t}.json",
            access_token=access_token,
        )
    )

    return LowcostMetadataInterface(
        locations=[types.Location(**l) for l in _req("locations")],
        sensors=[types.Sensor(**l) for l in _req("sensors")],
    )


class _DatetimeSeriesItem(BaseModel):
    from_datetime: pendulum.DateTime
    to_datetime: pendulum.DateTime


def _test_data_integrity(
    locations: list[types.Location],
    sensors: list[types.Sensor],
) -> None:
    location_ids = [s.location_id for s in locations]
    sensor_ids = [s.sensor_id for s in sensors]

    # unique ids
    assert len(set(location_ids)) == len(location_ids), "location ids are not unique"
    assert len(set(sensor_ids)) == len(sensor_ids), "sensor ids are not unique"

    # reference existence in sensors.json
    for s in sensors:
        for l in s.locations:
            assert l.location_id in location_ids, f"unknown location id {l.location_id}"

    # integrity of time series in sensors.json
    for s in sensors:
        location_timeseries = [_DatetimeSeriesItem(**l.dict()) for l in s.locations]

        # TEST TIME SERIES INTEGRITY OF "locations"

        for l in location_timeseries:
            assert (
                l.from_datetime < l.to_datetime
            ), f"from_datetime ({l.from_datetime}) has to smaller than to_datetime ({l.to_datetime})"

        for i in range(len(location_timeseries) - 1):
            l1, l2 = location_timeseries[i : i + 2]
            assert (
                l1.to_datetime <= l2.from_datetime
            ), f"time periods are overlapping: {l1.dict()}, {l1.dict()}"
