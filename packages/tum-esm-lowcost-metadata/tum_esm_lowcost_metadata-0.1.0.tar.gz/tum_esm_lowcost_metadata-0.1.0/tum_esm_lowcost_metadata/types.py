import pendulum
from pydantic import BaseModel, validator
from tum_esm_utils.validators import validate_float, validate_int, validate_str


class LocationColocation(BaseModel):
    colocation_type: str
    colocation_station_id: str

    _val_colocation_type = validator("colocation_type", pre=True, allow_reuse=True)(
        validate_str(allowed=["lfu", "midcost", "airquality"]),
    )
    _val_colocation_station_id = validator("colocation_station_id", pre=True, allow_reuse=True)(
        validate_str(),
    )

    class Config:
        extra = "ignore"


class Location(BaseModel):
    location_id: str
    details: str
    lon: float
    lat: float
    alt: float
    colocations: list[LocationColocation]

    # validators
    _val_location_id = validator("location_id", pre=True, allow_reuse=True)(
        validate_str(min_len=1, max_len=64, regex="^[A-Z0-9_]+$"),
    )
    _val_details = validator("details", pre=True, allow_reuse=True)(
        validate_str(min_len=3),
    )
    _val_lon = validator("lon", pre=True, allow_reuse=True)(
        validate_float(minimum=-180, maximum=180),
    )
    _val_lat = validator("lat", pre=True, allow_reuse=True)(
        validate_float(minimum=-90, maximum=90),
    )
    _val_alt = validator("alt", pre=True, allow_reuse=True)(
        validate_float(minimum=-20, maximum=10000),
    )

    class Config:
        extra = "ignore"


class SensorLocation(BaseModel):
    from_datetime: pendulum.DateTime
    to_datetime: pendulum.DateTime
    location_id: str
    mounting_orientation: int
    mounting_height: float

    # validators
    _val_date_string = validator(
        *["from_datetime", "to_datetime"],
        pre=True,
        allow_reuse=True,
    )(
        validate_str(is_rfc3339_datetime_string=True),
    )
    _val_location_id = validator("location_id", pre=True, allow_reuse=True)(
        validate_str(),
    )
    _val_mounting_orientation = validator("mounting_orientation", pre=True, allow_reuse=True)(
        validate_int(minimum=0, maximum=359),
    )
    _val_mounting_height = validator("mounting_height", pre=True, allow_reuse=True)(
        validate_float(),
    )

    class Config:
        extra = "ignore"


class Sensor(BaseModel):
    sensor_id: str
    sensor_type: str
    sensor_manufacturer: str
    details: str
    serial_number: str
    locations: list[SensorLocation]

    # validators
    _val_sensor_id = validator("sensor_id", pre=True, allow_reuse=True)(
        validate_str(min_len=1, max_len=64, regex="^[a-z0-9_]+$"),
    )
    _val_str = validator(
        "sensor_type", "sensor_manufacturer", "details", "serial_number", pre=True, allow_reuse=True
    )(
        validate_str(max_len=256),
    )

    class Config:
        extra = "ignore"


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

    class Config:
        extra = "ignore"
