# standard library
from dataclasses import dataclass, field


# dependencies
from pandas_dataclasses.core import get_attrs, get_name
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


def test_name() -> None:
    name = get_name(weather)

    assert name == "Weather at Tokyo"
