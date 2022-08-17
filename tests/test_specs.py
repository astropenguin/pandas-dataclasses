# standard library
from dataclasses import MISSING, dataclass
from typing import Dict


# dependencies
import numpy as np
from pandas_dataclasses.core.specs import DataSpec
from pandas_dataclasses.core.typing import Attr, Data, Index
from typing_extensions import Annotated as Ann
from typing_extensions import Literal as L


# test datasets
def name(stat: str, cat: str) -> Dict[str, str]:
    return {"Statistic": stat, "Category": cat}


@dataclass
class Weather:
    """Weather information at a location."""

    time: Ann[Index[L["M8[ns]"]], "Time in UTC"]
    temp_avg: Ann[Data[float], name("Temperature (degC)", "Average")]
    temp_max: Ann[Data[float], name("Temperature (degC)", "Maximum")]
    wind_avg: Ann[Data[float], name("Wind speed (m/s)", "Average")]
    wind_max: Ann[Data[float], name("Wind speed (m/s)", "Maximum")]
    location: Attr[str] = "Tokyo"
    longitude: Attr[float] = 139.69167
    latitude: Attr[float] = 35.68944


# test functions
def test_time() -> None:
    spec = DataSpec.from_dataclass(Weather).specs.of_index["time"]

    assert spec.name == "Time in UTC"
    assert spec.role == "index"
    assert spec.dtype == np.dtype("M8[ns]")
    assert spec.default is MISSING


def test_temp_avg() -> None:
    spec = DataSpec.from_dataclass(Weather).specs.of_data["temp_avg"]

    assert spec.name == name("Temperature (degC)", "Average")
    assert spec.role == "data"
    assert spec.dtype == np.float64
    assert spec.default is MISSING


def test_temp_max() -> None:
    spec = DataSpec.from_dataclass(Weather).specs.of_data["temp_max"]

    assert spec.name == name("Temperature (degC)", "Maximum")
    assert spec.role == "data"
    assert spec.dtype == np.float64
    assert spec.default is MISSING


def test_wind_avg() -> None:
    spec = DataSpec.from_dataclass(Weather).specs.of_data["wind_avg"]

    assert spec.name == name("Wind speed (m/s)", "Average")
    assert spec.role == "data"
    assert spec.dtype == np.float64
    assert spec.default is MISSING


def test_wind_max() -> None:
    spec = DataSpec.from_dataclass(Weather).specs.of_data["wind_max"]

    assert spec.name == name("Wind speed (m/s)", "Maximum")
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


def test_factory() -> None:
    assert DataSpec.from_dataclass(Weather).factory is None
