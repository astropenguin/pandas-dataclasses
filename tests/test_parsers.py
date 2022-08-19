# standard library
from dataclasses import dataclass


# dependencies
import numpy as np
import pandas as pd
from pandas_dataclasses.core.parsers import get_attrs, get_data, get_index
from pandas_dataclasses.core.specs import Spec
from pandas_dataclasses.core.typing import Attr, Data, Index
from typing_extensions import Annotated as Ann


# test datasets
@dataclass
class Weather:
    """Weather information at a location."""

    year: Ann[Index[int], "Year"]
    month: Ann[Index[int], "Month"]
    temp: Ann[Data[float], "Average temperature (deg C)"]
    humid: Ann[Data[float], "Average humidity (%)"]
    loc: Ann[Attr[str], "Location"] = "Tokyo"
    lon: Ann[Attr[float], "Longitude (deg)"] = 139.69167
    lat: Ann[Attr[float], "Latitude (deg)"] = 35.68944


weather = Weather(
    [2020, 2020, 2021, 2021, 2022],
    [1, 7, 1, 7, 1],
    [7.1, 24.3, 5.4, 25.9, 4.9],
    [65, 89, 57, 83, 52],
)


# test functions
def test_attrs() -> None:
    spec = Spec.from_dataclass(type(weather)) @ weather

    assert get_attrs(spec) == {
        "Location": "Tokyo",
        "Longitude (deg)": 139.69167,
        "Latitude (deg)": 35.68944,
    }


def test_data() -> None:
    spec = Spec.from_dataclass(type(weather)) @ weather
    data = get_data(spec)
    data_temp = data.get("Average temperature (deg C)")  # type: ignore
    data_humid = data.get("Average humidity (%)")  # type: ignore
    expected_temp = np.array(weather.temp, float)
    expected_humid = np.array(weather.humid, float)

    assert (data_temp == expected_temp).all()
    assert (data_humid == expected_humid).all()
    assert data_temp.dtype == expected_temp.dtype  # type: ignore
    assert data_humid.dtype == expected_humid.dtype  # type: ignore


def test_index() -> None:
    spec = Spec.from_dataclass(type(weather)) @ weather
    index = get_index(spec)
    expected = pd.MultiIndex.from_arrays(
        [weather.year, weather.month],
        names=["Year", "Month"],
    )

    assert (index == expected).all()
    assert (index.dtypes == expected.dtypes).all()  # type: ignore
    assert index.names == expected.names  # type: ignore
