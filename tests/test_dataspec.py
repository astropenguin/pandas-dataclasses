# standard library
from dataclasses import MISSING, dataclass


# dependencies
import numpy as np
from pandas_dataclasses.dataspec import DataSpec
from pandas_dataclasses.typing import Attr, Data, Index, Name, Named
from typing_extensions import Literal


# type hints
datetime = Literal["M8[ns]"]


# test datasets
@dataclass
class Weather:
    """Time-series weather information at a location."""

    time: Named[Index[datetime], "Time in UTC"]
    temperature: Named[Data[float], "Temperature (degC)"]
    humidity: Named[Data[float], "Humidity (percent)"]
    wind_speed: Named[Data[float], "Speed (m/s)"]
    wind_direction: Named[Data[float], "Direction (deg)"]
    location: Attr[str] = "Tokyo"
    longitude: Attr[float] = 139.69167
    latitude: Attr[float] = 35.68944
    name: Name[str] = "weather"


# test functions
def test_time() -> None:
    spec = DataSpec.from_dataclass(Weather).fields.index["time"]

    assert spec.type == "index"
    assert spec.name == "Time in UTC"
    assert spec.data.type == np.dtype("M8[ns]")
    assert spec.data.default is MISSING


def test_temperature() -> None:
    spec = DataSpec.from_dataclass(Weather).fields.data["temperature"]

    assert spec.type == "data"
    assert spec.name == "Temperature (degC)"
    assert spec.data.type == np.float64
    assert spec.data.default is MISSING


def test_humidity() -> None:
    spec = DataSpec.from_dataclass(Weather).fields.data["humidity"]

    assert spec.type == "data"
    assert spec.name == "Humidity (percent)"
    assert spec.data.type == np.float64
    assert spec.data.default is MISSING


def test_wind_speed() -> None:
    spec = DataSpec.from_dataclass(Weather).fields.data["wind_speed"]

    assert spec.type == "data"
    assert spec.name == "Speed (m/s)"
    assert spec.data.type == np.float64
    assert spec.data.default is MISSING


def test_wind_direction() -> None:
    spec = DataSpec.from_dataclass(Weather).fields.data["wind_direction"]

    assert spec.type == "data"
    assert spec.name == "Direction (deg)"
    assert spec.data.type == np.float64
    assert spec.data.default is MISSING


def test_location() -> None:
    spec = DataSpec.from_dataclass(Weather).fields.attr["location"]

    assert spec.type == "attr"
    assert spec.name == "location"
    assert spec.data.type is str
    assert spec.data.default == "Tokyo"


def test_longitude() -> None:
    spec = DataSpec.from_dataclass(Weather).fields.attr["longitude"]

    assert spec.type == "attr"
    assert spec.name == "longitude"
    assert spec.data.type is float
    assert spec.data.default == 139.69167


def test_latitude() -> None:
    spec = DataSpec.from_dataclass(Weather).fields.attr["latitude"]

    assert spec.type == "attr"
    assert spec.name == "latitude"
    assert spec.data.type is float
    assert spec.data.default == 35.68944


def test_name() -> None:
    spec = DataSpec.from_dataclass(Weather).fields.name["name"]

    assert spec.type == "name"
    assert spec.name == "name"
    assert spec.data.type is str
    assert spec.data.default == "weather"
