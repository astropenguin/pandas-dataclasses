# standard library
from dataclasses import dataclass
from typing import ClassVar


# dependencies
import numpy as np
import pandas as pd
from pandas_dataclasses.pandas.series import AsSeries
from pandas_dataclasses.typing import Attr, Data, Index, Name
from typing_extensions import Annotated as Ann
from typing_extensions import Literal as L


# test datasets
class CustomSeries(pd.Series):
    """Custom pandas Series."""

    __slots__ = ()


@dataclass
class Temperature(AsSeries):
    """Temperature information at a location."""

    time: Ann[Index[L["M8[ns]"]], "Time in UTC"]
    data: Data[float]
    loc: Ann[Attr[str], "Location"] = "Tokyo"
    lon: Ann[Attr[float], "Longitude (deg)"] = 139.69167
    lat: Ann[Attr[float], "Latitude (deg)"] = 35.68944
    name: Name[str] = "Temperature (deg C)"

    __pandas_factory__: ClassVar = CustomSeries


time = pd.date_range("2020-01", "2020-06", freq="MS")
data = np.array([7.1, 8.3, 10.7, 12.8, 19.5, 23.2])
temperature = Temperature.new(time, data)


# test functions
def test_attrs() -> None:
    assert temperature.attrs == {
        "Location": "Tokyo",
        "Longitude (deg)": 139.69167,
        "Latitude (deg)": 35.68944,
    }


def test_data() -> None:
    assert temperature.to_numpy() is data
    assert temperature.name == "Temperature (deg C)"
    assert temperature.dtype == np.float64


def test_index() -> None:
    index = temperature.index

    assert index.to_numpy() is time.to_numpy()
    assert index.name == "Time in UTC"
    assert index.dtype == np.dtype("M8[ns]")


def test_instance() -> None:
    assert isinstance(temperature, CustomSeries)
