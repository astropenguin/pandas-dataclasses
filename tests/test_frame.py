# standard library
from dataclasses import dataclass
from typing import ClassVar


# dependencies
import numpy as np
import pandas as pd
from pandas_dataclasses.pandas.frame import AsDataFrame
from pandas_dataclasses.typing import Attr, Data, Index
from typing_extensions import Annotated as Ann


# test datasets
class CustomFrame(pd.DataFrame):
    """Custom pandas DataFrame."""

    __slots__ = ()


@dataclass
class Weather(AsDataFrame):
    """Weather information at a location."""

    year: Ann[Index[int], "Year"]
    month: Ann[Index[int], "Month"]
    temp: Ann[Data[float], "Average temperature (deg C)"]
    humid: Ann[Data[float], "Average humidity (%)"]
    loc: Ann[Attr[str], "Location"] = "Tokyo"
    lon: Ann[Attr[float], "Longitude (deg)"] = 139.69167
    lat: Ann[Attr[float], "Latitude (deg)"] = 35.68944

    __pandas_factory__: ClassVar = CustomFrame


year = np.array([2020, 2020, 2021, 2021, 2022])
month = np.array([1, 7, 1, 7, 1])
temp = np.array([7.1, 24.3, 5.4, 25.9, 4.9])
humid = np.array([65, 89, 57, 83, 52])
weather = Weather.new(year, month, temp, humid)


# test functions
def test_attrs() -> None:
    assert weather.attrs == {
        "Location": "Tokyo",
        "Longitude (deg)": 139.69167,
        "Latitude (deg)": 35.68944,
    }


def test_data() -> None:
    data_0 = weather.iloc[:, 0]
    data_1 = weather.iloc[:, 1]

    assert (data_0 == temp).all()
    assert (data_1 == humid).all()
    assert data_0.dtype == np.dtype("float64")
    assert data_1.dtype == np.dtype("float64")
    assert data_0.name == "Average temperature (deg C)"
    assert data_1.name == "Average humidity (%)"


def test_index() -> None:
    index_0 = weather.index.get_level_values(0)
    index_1 = weather.index.get_level_values(1)

    assert (index_0 == year).all()
    assert (index_1 == month).all()
    assert index_0.dtype == np.dtype("int64")
    assert index_1.dtype == np.dtype("int64")
    assert index_0.name == "Year"
    assert index_1.name == "Month"


def test_instance() -> None:
    assert isinstance(weather, CustomFrame)
