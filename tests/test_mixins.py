# standard library
from dataclasses import dataclass
from typing import Any


# dependencies
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal
from data import Weather, weather, df_weather_true, ser_weather_true
from pandas_dataclasses import As, AsFrame, AsSeries


# test data
def factory(*args: Any, **kwargs: Any) -> pd.Series:  # type: ignore
    return pd.Series(*args, **kwargs)  # type: ignore


class CustomDataFrame(pd.DataFrame):
    pass


class CustomSeries(pd.Series):  # type: ignore
    pass


@dataclass
class DataFrameWeather(Weather, AsFrame):
    pass


@dataclass
class CustomDataFrameWeather(Weather, As[CustomDataFrame]):
    pass


@dataclass
class SeriesWeather(Weather, AsSeries):
    pass


@dataclass
class FactorySeriesWeather(Weather, AsSeries, factory=factory):
    pass


@dataclass
class CustomSeriesWeather(Weather, As[CustomSeries]):
    pass


@dataclass
class FloatSeriesWeather(Weather, As["pd.Series[float]"], factory=pd.Series):
    pass


# test functions
def test_dataframe_weather() -> None:
    df_weather = DataFrameWeather.new(
        year=weather.year,
        month=weather.month,
        temp_avg=weather.temp_avg,
        temp_max=weather.temp_max,
        wind_avg=weather.wind_avg,
        wind_max=weather.wind_max,
    )

    assert isinstance(df_weather, pd.DataFrame)
    assert_frame_equal(df_weather, df_weather_true)


def test_custom_dataframe_weather() -> None:
    df_weather = CustomDataFrameWeather.new(
        year=weather.year,
        month=weather.month,
        temp_avg=weather.temp_avg,
        temp_max=weather.temp_max,
        wind_avg=weather.wind_avg,
        wind_max=weather.wind_max,
    )

    assert isinstance(df_weather, CustomDataFrame)
    assert_frame_equal(df_weather, df_weather_true, check_frame_type=False)


def test_series_weather() -> None:
    ser_weather = SeriesWeather.new(
        year=weather.year,
        month=weather.month,
        temp_avg=weather.temp_avg,
        temp_max=weather.temp_max,
        wind_avg=weather.wind_avg,
        wind_max=weather.wind_max,
    )

    assert isinstance(ser_weather, pd.Series)
    assert_series_equal(ser_weather, ser_weather_true)


def test_factory_series_weather() -> None:
    ser_weather = FactorySeriesWeather.new(
        year=weather.year,
        month=weather.month,
        temp_avg=weather.temp_avg,
        temp_max=weather.temp_max,
        wind_avg=weather.wind_avg,
        wind_max=weather.wind_max,
    )

    assert isinstance(ser_weather, pd.Series)
    assert_series_equal(ser_weather, ser_weather_true)


def test_custom_series_weather() -> None:
    ser_weather = CustomSeriesWeather.new(
        year=weather.year,
        month=weather.month,
        temp_avg=weather.temp_avg,
        temp_max=weather.temp_max,
        wind_avg=weather.wind_avg,
        wind_max=weather.wind_max,
    )

    assert isinstance(ser_weather, CustomSeries)
    assert_series_equal(ser_weather, ser_weather_true, check_series_type=False)


def test_float_series_weather() -> None:
    ser_weather = FloatSeriesWeather.new(
        year=weather.year,
        month=weather.month,
        temp_avg=weather.temp_avg,
        temp_max=weather.temp_max,
        wind_avg=weather.wind_avg,
        wind_max=weather.wind_max,
    )

    assert isinstance(ser_weather, pd.Series)
    assert_series_equal(ser_weather, ser_weather_true, check_series_type=False)
