# standard library
from dataclasses import dataclass, field


# dependencies
import numpy as np
import pandas as pd
from pandas_dataclasses.core import get_attrs, get_data, get_index, get_name
from pandas_dataclasses.typing import Attr, Data, Index, Name
from typing_extensions import Annotated as Named


# test datasets
@dataclass
class Weather:
    """Weather information at a location."""

    year: Named[Index[int], "Year"]
    month: Named[Index[int], "Month"]
    temperature: Named[Data[float], "Average temperature (deg C)"]
    humidity: Named[Data[float], "Average humidity (%)"]
    location: Named[Attr[str], "Location"] = "Tokyo"
    longitude: Named[Attr[float], "Longitude (deg)"] = 139.69167
    latitude: Named[Attr[float], "Latitude (deg)"] = 35.68944
    name: Name[str] = field(init=False)

    def __post_init__(self) -> None:
        self.name = f"Weather at {self.location}"


weather = Weather(
    [2020, 2020, 2021, 2021, 2022],
    [1, 7, 1, 7, 1],
    [7.1, 24.3, 5.4, 25.9, 4.9],
    [65, 89, 57, 83, 52],
)


# test functions
def test_attrs() -> None:
    attrs = get_attrs(weather)

    assert attrs == {
        "Location": "Tokyo",
        "Longitude (deg)": 139.69167,
        "Latitude (deg)": 35.68944,
    }


def test_data() -> None:
    data = get_data(weather)
    data_temp = data.get("Average temperature (deg C)")  # type: ignore
    data_humid = data.get("Average humidity (%)")  # type: ignore
    expected_temp = np.array(weather.temperature, float)
    expected_humid = np.array(weather.humidity, float)

    assert (data_temp == expected_temp).all()
    assert (data_humid == expected_humid).all()
    assert data_temp.dtype == expected_temp.dtype  # type: ignore
    assert data_humid.dtype == expected_humid.dtype  # type: ignore


def test_index() -> None:
    index = get_index(weather)
    expected = pd.MultiIndex.from_arrays(
        [weather.year, weather.month],
        names=["Year", "Month"],
    )

    assert (index == expected).all()
    assert (index.dtypes == expected.dtypes).all()  # type: ignore
    assert index.names == expected.names  # type: ignore


def test_name() -> None:
    name = get_name(weather)

    assert name == "Weather at Tokyo"
