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


class UserFrame(pd.DataFrame):
    pass


class UserSeries(pd.Series):  # type: ignore
    pass


@dataclass
class Frame(Weather, AsFrame):
    pass


@dataclass
class CustomFrame(Weather, As[UserFrame]):
    pass


@dataclass
class Series(Weather, AsSeries):
    pass


@dataclass
class CustomSeries(Weather, As[UserSeries]):
    pass


@dataclass
class FactorySeries(Weather, AsSeries, factory=factory):
    pass


@dataclass
class FloatSeries(Weather, As["pd.Series[float]"], factory=pd.Series):
    pass


# test functions
def test_frame() -> None:
    df_weather = Frame.new(
        year=weather.year,
        month=weather.month,
        temp_avg=weather.temp_avg,
        temp_max=weather.temp_max,
        wind_avg=weather.wind_avg,
        wind_max=weather.wind_max,
    )

    assert isinstance(df_weather, pd.DataFrame)
    assert_frame_equal(df_weather, df_weather_true)


def test_custom_frame() -> None:
    df_weather = CustomFrame.new(
        year=weather.year,
        month=weather.month,
        temp_avg=weather.temp_avg,
        temp_max=weather.temp_max,
        wind_avg=weather.wind_avg,
        wind_max=weather.wind_max,
    )

    assert isinstance(df_weather, UserFrame)
    assert_frame_equal(df_weather, df_weather_true, check_frame_type=False)


def test_series() -> None:
    ser_weather = Series.new(
        year=weather.year,
        month=weather.month,
        temp_avg=weather.temp_avg,
        temp_max=weather.temp_max,
        wind_avg=weather.wind_avg,
        wind_max=weather.wind_max,
    )

    assert isinstance(ser_weather, pd.Series)
    assert_series_equal(ser_weather, ser_weather_true)


def test_custom_series() -> None:
    ser_weather = CustomSeries.new(
        year=weather.year,
        month=weather.month,
        temp_avg=weather.temp_avg,
        temp_max=weather.temp_max,
        wind_avg=weather.wind_avg,
        wind_max=weather.wind_max,
    )

    assert isinstance(ser_weather, UserSeries)
    assert_series_equal(ser_weather, ser_weather_true, check_series_type=False)


def test_factory_series() -> None:
    ser_weather = FactorySeries.new(
        year=weather.year,
        month=weather.month,
        temp_avg=weather.temp_avg,
        temp_max=weather.temp_max,
        wind_avg=weather.wind_avg,
        wind_max=weather.wind_max,
    )

    assert isinstance(ser_weather, pd.Series)
    assert_series_equal(ser_weather, ser_weather_true)


def test_float_series() -> None:
    ser_weather = FloatSeries.new(
        year=weather.year,
        month=weather.month,
        temp_avg=weather.temp_avg,
        temp_max=weather.temp_max,
        wind_avg=weather.wind_avg,
        wind_max=weather.wind_max,
    )

    assert isinstance(ser_weather, pd.Series)
    assert_series_equal(ser_weather, ser_weather_true, check_series_type=False)
