__all__ = ["Weather", "weather", "df_weather_true", "ser_weather_true"]


# standard library
from dataclasses import dataclass, field
from typing import Any


# dependencies
import pandas as pd
from pandas_dataclasses import Attr, Column, Data, Index, Multiple
from typing_extensions import Annotated as Ann


# test dataclass and object
@dataclass
class Weather:
    """Weather information."""

    year: Ann[Index[int], "Year"]
    """Year of the measured time."""

    month: Ann[Index[int], "Month"]
    """Month of the measured time."""

    meas: Ann[Column[None], "Measurement"] = field(init=False, repr=False)
    """Name of the measurement."""

    stat: Ann[Column[None], "Statistic"] = field(init=False, repr=False)
    """Name of the statistic."""

    temp_avg: Ann[Data[float], ("Temperature ({.temp_unit})", "Average")]
    """Monthly average temperature with given units."""

    temp_max: Ann[Data[float], ("Temperature ({.temp_unit})", "Maximum")]
    """Monthly maximum temperature with given units."""

    wind_avg: Ann[Data[float], ("Wind speed ({.wind_unit})", "Average")]
    """Monthly average wind speed with given units."""

    wind_max: Ann[Data[float], ("Wind speed ({.wind_unit})", "Maximum")]
    """Monthly maximum wind speed with given units."""

    loc: Ann[Attr[str], "Location"] = "Tokyo"
    """Name of the measured location."""

    lon: Ann[Attr[float], "Longitude ({.lon_unit})"] = 139.69167
    """Longitude at the measured location."""

    lat: Ann[Attr[float], "Latitude ({.lat_unit})"] = 35.68944
    """Latitude at the measured location."""

    temp_unit: str = "deg C"
    """Units of the temperature."""

    wind_unit: str = "m/s"
    """Units of the wind speed."""

    lon_unit: str = "deg"
    """Units of the longitude."""

    lat_unit: str = "deg"
    """Units of the latitude."""

    attrs: Multiple[Attr[Any]] = field(default_factory=dict)
    """Other attributes."""


weather = Weather(
    [2020, 2020, 2021, 2021, 2022],
    [1, 7, 1, 7, 1],
    [7.1, 24.3, 5.4, 25.9, 4.9],
    [11.1, 27.7, 10.3, 30.3, 9.4],
    [2.4, 3.1, 2.3, 2.4, 2.6],
    [8.8, 10.2, 10.7, 9.0, 8.8],
)


# expected pandas data
df_weather_true = pd.DataFrame(
    data={
        ("Temperature (deg C)", "Average"): [7.1, 24.3, 5.4, 25.9, 4.9],
        ("Temperature (deg C)", "Maximum"): [11.1, 27.7, 10.3, 30.3, 9.4],
        ("Wind speed (m/s)", "Average"): [2.4, 3.1, 2.3, 2.4, 2.6],
        ("Wind speed (m/s)", "Maximum"): [8.8, 10.2, 10.7, 9.0, 8.8],
    },
    index=pd.MultiIndex.from_arrays(
        [
            [2020, 2020, 2021, 2021, 2022],
            [1, 7, 1, 7, 1],
        ],
        names=("Year", "Month"),
    ),
    columns=pd.MultiIndex.from_tuples(
        [
            ("Temperature (deg C)", "Average"),
            ("Temperature (deg C)", "Maximum"),
            ("Wind speed (m/s)", "Average"),
            ("Wind speed (m/s)", "Maximum"),
        ],
        names=("Measurement", "Statistic"),
    ),
)
df_weather_true.attrs = {
    "Location": "Tokyo",
    "Longitude (deg)": 139.69167,
    "Latitude (deg)": 35.68944,
}


ser_weather_true: "pd.Series[Any]" = pd.Series(
    data=[7.1, 24.3, 5.4, 25.9, 4.9],
    index=pd.MultiIndex.from_arrays(
        [
            [2020, 2020, 2021, 2021, 2022],
            [1, 7, 1, 7, 1],
        ],
        names=("Year", "Month"),
    ),
    name=("Temperature (deg C)", "Average"),
)
ser_weather_true.attrs = {
    "Location": "Tokyo",
    "Longitude (deg)": 139.69167,
    "Latitude (deg)": 35.68944,
}
