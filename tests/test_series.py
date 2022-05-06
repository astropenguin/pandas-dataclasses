# standard library
from dataclasses import dataclass


# dependencies
import numpy as np
import pandas as pd
from pandas_dataclasses.pandas.series import AsSeries
from pandas_dataclasses.typing import Attr, Data, Index, Name
from typing_extensions import Annotated, Literal


# type hints
datetime = Literal["M8[ns]"]


# test datasets
@dataclass
class Temperature(AsSeries):
    """Time-series temperature information at a location."""

    time: Annotated[Index[datetime], "Time in UTC"]
    temperature: Data[float]
    location: Attr[str] = "Tokyo"
    longitude: Attr[float] = 139.69167
    latitude: Attr[float] = 35.68944
    name: Name[str] = "Temperature (deg C)"


time = pd.date_range("2020-01", "2020-06", freq="MS")
temp = np.array([7.1, 8.3, 10.7, 12.8, 19.5, 23.2])


# test functions
def test_index() -> None:
    index = Temperature.new(time, temp).index

    assert index.to_numpy() is time.to_numpy()
    assert index.name == "Time in UTC"
    assert index.dtype == np.dtype("M8[ns]")


def test_data() -> None:
    data = Temperature.new(time, temp)

    assert data.to_numpy() is temp
    assert data.name == "Temperature (deg C)"
    assert data.dtype == np.float64


def test_attrs() -> None:
    attrs = Temperature.new(time, temp).attrs

    assert attrs["location"] == "Tokyo"
    assert attrs["longitude"] == 139.69167
    assert attrs["latitude"] == 35.68944
