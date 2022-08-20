# standard library
from dataclasses import asdict, dataclass


# dependencies
import pandas as pd
from data import Weather, weather, df_weather_true, ser_weather_true
from pandas_dataclasses.core.mixins import As, AsDataFrame, AsSeries


# test data
class CustomDataFrame(pd.DataFrame):
    pass


class CustomSeries(pd.Series):
    pass


@dataclass
class DataFrameWeather(Weather, AsDataFrame):
    pass


@dataclass
class SeriesWeather(Weather, AsSeries):
    pass


@dataclass
class CustomDataFrameWeather(Weather, As[CustomDataFrame]):
    pass


@dataclass
class CustomSeriesWeather(Weather, As[CustomSeries]):
    pass


# test functions
def test_dataframe_weather() -> None:
    df_weather = DataFrameWeather.new(**asdict(weather))

    assert isinstance(df_weather, pd.DataFrame)
    assert (df_weather == df_weather_true).all().all()


def test_custom_dataframe_weather() -> None:
    df_weather = CustomDataFrameWeather.new(**asdict(weather))

    assert isinstance(df_weather, CustomDataFrame)
    assert (df_weather == df_weather_true).all().all()


def test_series_weather() -> None:
    ser_weather = SeriesWeather.new(**asdict(weather))

    assert isinstance(ser_weather, pd.Series)
    assert (ser_weather == ser_weather_true).all()


def test_custom_series_weather() -> None:
    ser_weather = CustomSeriesWeather.new(**asdict(weather))

    assert isinstance(ser_weather, CustomSeries)
    assert (ser_weather == ser_weather_true).all()
