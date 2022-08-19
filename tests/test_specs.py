# standard library
from dataclasses import MISSING, dataclass
from typing import Dict


# dependencies
import numpy as np
from pandas_dataclasses.core.specs import Spec
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
    field = Spec.from_dataclass(Weather).fields.of_index[0]

    assert field.id == "time"
    assert field.name == "Time in UTC"
    assert field.hashable_name == "Time in UTC"
    assert field.role == "index"
    assert field.type == Ann[Index[L["M8[ns]"]], "Time in UTC"]
    assert field.dtype == np.dtype("M8[ns]")
    assert field.default is MISSING


def test_temp_avg() -> None:
    field = Spec.from_dataclass(Weather).fields.of_data[0]

    assert field.id == "temp_avg"
    assert field.name == name("Temperature (degC)", "Average")
    assert field.hashable_name == ("Temperature (degC)", "Average")
    assert field.role == "data"
    assert field.type == Ann[Data[float], name("Temperature (degC)", "Average")]
    assert field.dtype == np.float64
    assert field.default is MISSING


def test_temp_max() -> None:
    field = Spec.from_dataclass(Weather).fields.of_data[1]

    assert field.id == "temp_max"
    assert field.name == name("Temperature (degC)", "Maximum")
    assert field.hashable_name == ("Temperature (degC)", "Maximum")
    assert field.role == "data"
    assert field.type == Ann[Data[float], name("Temperature (degC)", "Maximum")]
    assert field.dtype == np.float64
    assert field.default is MISSING


def test_wind_avg() -> None:
    field = Spec.from_dataclass(Weather).fields.of_data[2]

    assert field.id == "wind_avg"
    assert field.name == name("Wind speed (m/s)", "Average")
    assert field.hashable_name == ("Wind speed (m/s)", "Average")
    assert field.role == "data"
    assert field.type == Ann[Data[float], name("Wind speed (m/s)", "Average")]
    assert field.dtype == np.float64
    assert field.default is MISSING


def test_wind_max() -> None:
    field = Spec.from_dataclass(Weather).fields.of_data[3]

    assert field.id == "wind_max"
    assert field.name == name("Wind speed (m/s)", "Maximum")
    assert field.hashable_name == ("Wind speed (m/s)", "Maximum")
    assert field.role == "data"
    assert field.type == Ann[Data[float], name("Wind speed (m/s)", "Maximum")]
    assert field.dtype == np.float64
    assert field.default is MISSING


def test_location() -> None:
    field = Spec.from_dataclass(Weather).fields.of_attr[0]

    assert field.id == "location"
    assert field.name == "location"
    assert field.hashable_name == "location"
    assert field.role == "attr"
    assert field.type == Attr[str]
    assert field.dtype is None
    assert field.default == "Tokyo"


def test_longitude() -> None:
    field = Spec.from_dataclass(Weather).fields.of_attr[1]

    assert field.id == "longitude"
    assert field.name == "longitude"
    assert field.hashable_name == "longitude"
    assert field.role == "attr"
    assert field.type == Attr[float]
    assert field.dtype is None
    assert field.default == 139.69167


def test_latitude() -> None:
    field = Spec.from_dataclass(Weather).fields.of_attr[2]

    assert field.id == "latitude"
    assert field.name == "latitude"
    assert field.hashable_name == "latitude"
    assert field.role == "attr"
    assert field.type == Attr[float]
    assert field.dtype is None
    assert field.default == 35.68944


def test_factory() -> None:
    assert Spec.from_dataclass(Weather).factory is None
