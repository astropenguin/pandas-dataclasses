# standard library
from dataclasses import MISSING, dataclass


# dependencies
import numpy as np
from pandas_dataclasses.dataspec import DataSpec
from pandas_dataclasses.typing import Attr, Data, Index, Name, Named


# test datasets
@dataclass
class Weather:
    """Time-series weather information at a location."""

    time: Named[Index[np.datetime64], "Time in UTC"]
    temperature: Named[Data[float], "Temperature (degC)"]
    humidity: Named[Data[float], "Humidity (percent)"]
    wind_speed: Named[Data[float], "Speed (m/s)"]
    wind_direction: Named[Data[float], "Direction (deg)"]
    location: Attr[str] = "Tokyo"
    longitude: Attr[float] = 0.0
    latitude: Attr[float] = 0.0
    name: Name[str] = "weather"


# test functions
def test_time() -> None:
    spec = DataSpec.from_dataclass(Weather).indexes[0]

    assert spec.type == "index"
    assert spec.name == "Time in UTC"
    assert spec.data.type == np.datetime64
    assert spec.data.default is MISSING


def test_temperature() -> None:
    spec = DataSpec.from_dataclass(Weather).data[0]

    assert spec.type == "data"
    assert spec.name == "Temperature (degC)"
    assert spec.data.type == np.float64
    assert spec.data.default is MISSING


def test_humidity() -> None:
    spec = DataSpec.from_dataclass(Weather).data[1]

    assert spec.type == "data"
    assert spec.name == "Humidity (percent)"
    assert spec.data.type == np.float64
    assert spec.data.default is MISSING


def test_wind_speed() -> None:
    spec = DataSpec.from_dataclass(Weather).data[2]

    assert spec.type == "data"
    assert spec.name == "Speed (m/s)"
    assert spec.data.type == np.float64
    assert spec.data.default is MISSING


def test_wind_direction() -> None:
    spec = DataSpec.from_dataclass(Weather).data[3]

    assert spec.type == "data"
    assert spec.name == "Direction (deg)"
    assert spec.data.type == np.float64
    assert spec.data.default is MISSING


def test_location() -> None:
    spec = DataSpec.from_dataclass(Weather).attrs[0]

    assert spec.type == "attr"
    assert spec.name == "location"
    assert spec.data.type is str
    assert spec.data.default == "Tokyo"


def test_longitude() -> None:
    spec = DataSpec.from_dataclass(Weather).attrs[1]

    assert spec.type == "attr"
    assert spec.name == "longitude"
    assert spec.data.type is float
    assert spec.data.default == 0.0


def test_latitude() -> None:
    spec = DataSpec.from_dataclass(Weather).attrs[2]

    assert spec.type == "attr"
    assert spec.name == "latitude"
    assert spec.data.type is float
    assert spec.data.default == 0.0


def test_name() -> None:
    spec = DataSpec.from_dataclass(Weather).names[0]

    assert spec.type == "name"
    assert spec.name == "name"
    assert spec.data.type is str
    assert spec.data.default == "weather"
