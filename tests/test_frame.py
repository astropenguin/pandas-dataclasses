# standard library
from dataclasses import dataclass


# dependencies
import numpy as np
from pandas_dataclasses.pandas.frame import AsDataFrame
from pandas_dataclasses.typing import Attr, Data, Index
from typing_extensions import Annotated as Named


# test datasets
@dataclass
class Weather(AsDataFrame):
    """Weather information at a location."""

    year: Named[Index[int], "Year"]
    month: Named[Index[int], "Month"]
    temp: Named[Data[float], "Average temperature (deg C)"]
    humid: Named[Data[float], "Average humidity (%)"]
    loc: Named[Attr[str], "Location"] = "Tokyo"
    lon: Named[Attr[float], "Longitude (deg)"] = 139.69167
    lat: Named[Attr[float], "Latitude (deg)"] = 35.68944


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
