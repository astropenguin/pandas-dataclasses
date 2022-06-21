# standard library
from dataclasses import MISSING, dataclass


# dependencies
import numpy as np
from pandas_dataclasses.specs import DataSpec
from pandas_dataclasses.typing import Attr, Data, Index, Name
from typing_extensions import Annotated as Ann
from typing_extensions import Literal as L


# test datasets
@dataclass
class Weather:
    """Weather information at a location."""

    time: Ann[Index[L["M8[ns]"]], "Time in UTC"]
    temperature: Ann[Data[float], "Temperature (degC)"]
    humidity: Ann[Data[float], "Humidity (percent)"]
    wind_speed: Ann[Data[float], "Speed (m/s)"]
    wind_direction: Ann[Data[float], "Direction (deg)"]
    location: Attr[str] = "Tokyo"
    longitude: Attr[float] = 139.69167
    latitude: Attr[float] = 35.68944
    name: Name[str] = "weather"


# test functions
def test_time() -> None:
    spec = DataSpec.from_dataclass(Weather).specs.of_index["time"]

    assert spec.name == "Time in UTC"
    assert spec.role == "index"
    assert spec.dtype == np.dtype("M8[ns]")
    assert spec.default is MISSING


def test_temperature() -> None:
    spec = DataSpec.from_dataclass(Weather).specs.of_data["temperature"]

    assert spec.name == "Temperature (degC)"
    assert spec.role == "data"
    assert spec.dtype == np.float64
    assert spec.default is MISSING


def test_humidity() -> None:
    spec = DataSpec.from_dataclass(Weather).specs.of_data["humidity"]

    assert spec.name == "Humidity (percent)"
    assert spec.role == "data"
    assert spec.dtype == np.float64
    assert spec.default is MISSING


def test_wind_speed() -> None:
    spec = DataSpec.from_dataclass(Weather).specs.of_data["wind_speed"]

    assert spec.name == "Speed (m/s)"
    assert spec.role == "data"
    assert spec.dtype == np.float64
    assert spec.default is MISSING


def test_wind_direction() -> None:
    spec = DataSpec.from_dataclass(Weather).specs.of_data["wind_direction"]

    assert spec.name == "Direction (deg)"
    assert spec.role == "data"
    assert spec.dtype == np.float64
    assert spec.default is MISSING


def test_location() -> None:
    spec = DataSpec.from_dataclass(Weather).specs.of_attr["location"]

    assert spec.name == "location"
    assert spec.role == "attr"
    assert spec.type is str
    assert spec.default == "Tokyo"


def test_longitude() -> None:
    spec = DataSpec.from_dataclass(Weather).specs.of_attr["longitude"]

    assert spec.name == "longitude"
    assert spec.role == "attr"
    assert spec.type is float
    assert spec.default == 139.69167


def test_latitude() -> None:
    spec = DataSpec.from_dataclass(Weather).specs.of_attr["latitude"]

    assert spec.name == "latitude"
    assert spec.role == "attr"
    assert spec.type is float
    assert spec.default == 35.68944


def test_name() -> None:
    spec = DataSpec.from_dataclass(Weather).specs.of_name["name"]

    assert spec.name == "name"
    assert spec.role == "name"
    assert spec.type is str
    assert spec.default == "weather"


def test_factory() -> None:
    assert DataSpec.from_dataclass(Weather).factory is None
