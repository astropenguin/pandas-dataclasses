# standard library
from dataclasses import MISSING, dataclass


# dependencies
import numpy as np
from pandas_dataclasses.specs import DataSpec
from pandas_dataclasses.typing import Attr, Data, Index, Name
from typing_extensions import Annotated, Literal


# type hints
datetime = Literal["M8[ns]"]


# test datasets
@dataclass
class Weather:
    """Time-series weather information at a location."""

    time: Annotated[Index[datetime], "Time in UTC"]
    temperature: Annotated[Data[float], "Temperature (degC)"]
    humidity: Annotated[Data[float], "Humidity (percent)"]
    wind_speed: Annotated[Data[float], "Speed (m/s)"]
    wind_direction: Annotated[Data[float], "Direction (deg)"]
    location: Attr[str] = "Tokyo"
    longitude: Attr[float] = 139.69167
    latitude: Attr[float] = 35.68944
    name: Name[str] = "weather"


# test functions
def test_time() -> None:
    spec = DataSpec.from_dataclass(Weather).fields.of_index["time"]

    assert spec.role == "index"
    assert spec.name == "Time in UTC"
    assert spec.data.type == np.dtype("M8[ns]")
    assert spec.data.default is MISSING


def test_temperature() -> None:
    spec = DataSpec.from_dataclass(Weather).fields.of_data["temperature"]

    assert spec.role == "data"
    assert spec.name == "Temperature (degC)"
    assert spec.data.type == np.float64
    assert spec.data.default is MISSING


def test_humidity() -> None:
    spec = DataSpec.from_dataclass(Weather).fields.of_data["humidity"]

    assert spec.role == "data"
    assert spec.name == "Humidity (percent)"
    assert spec.data.type == np.float64
    assert spec.data.default is MISSING


def test_wind_speed() -> None:
    spec = DataSpec.from_dataclass(Weather).fields.of_data["wind_speed"]

    assert spec.role == "data"
    assert spec.name == "Speed (m/s)"
    assert spec.data.type == np.float64
    assert spec.data.default is MISSING


def test_wind_direction() -> None:
    spec = DataSpec.from_dataclass(Weather).fields.of_data["wind_direction"]

    assert spec.role == "data"
    assert spec.name == "Direction (deg)"
    assert spec.data.type == np.float64
    assert spec.data.default is MISSING


def test_location() -> None:
    spec = DataSpec.from_dataclass(Weather).fields.of_attr["location"]

    assert spec.role == "attr"
    assert spec.name == "location"
    assert spec.data.type is str
    assert spec.data.default == "Tokyo"


def test_longitude() -> None:
    spec = DataSpec.from_dataclass(Weather).fields.of_attr["longitude"]

    assert spec.role == "attr"
    assert spec.name == "longitude"
    assert spec.data.type is float
    assert spec.data.default == 139.69167


def test_latitude() -> None:
    spec = DataSpec.from_dataclass(Weather).fields.of_attr["latitude"]

    assert spec.role == "attr"
    assert spec.name == "latitude"
    assert spec.data.type is float
    assert spec.data.default == 35.68944


def test_name() -> None:
    spec = DataSpec.from_dataclass(Weather).fields.of_name["name"]

    assert spec.role == "name"
    assert spec.name == "name"
    assert spec.data.type is str
    assert spec.data.default == "weather"
