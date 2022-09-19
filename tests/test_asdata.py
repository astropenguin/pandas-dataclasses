# standard library
from typing import cast


# dependencies
import pandas as pd
from data import Weather, weather, df_weather_true, ser_weather_true
from pandas_dataclasses.core.asdata import (
    asdataframe,
    asseries,
    get_attrs,
    get_columns,
    get_data,
    get_index,
)
from pandas_dataclasses.core.specs import Spec


# test data
spec = Spec.from_dataclass(Weather) @ weather


# test functions
def test_asseries() -> None:
    ser_weather = asseries(weather)

    assert ser_weather.attrs == ser_weather_true.attrs
    assert ser_weather.name == ser_weather_true.name
    assert ser_weather.dtype == ser_weather_true.dtype
    assert (ser_weather == ser_weather_true).all()

    assert ser_weather.index.name == ser_weather_true.index.name
    assert ser_weather.index.dtype == ser_weather_true.index.dtype
    assert (ser_weather.index == ser_weather_true.index).all()


def test_asdataframe() -> None:
    df_weather = asdataframe(weather)

    assert df_weather.attrs == df_weather_true.attrs
    assert df_weather.iloc[:, 0].dtype == df_weather_true.iloc[:, 0].dtype
    assert df_weather.iloc[:, 1].dtype == df_weather_true.iloc[:, 1].dtype
    assert df_weather.iloc[:, 2].dtype == df_weather_true.iloc[:, 2].dtype
    assert df_weather.iloc[:, 3].dtype == df_weather_true.iloc[:, 3].dtype
    assert (df_weather == df_weather_true).all().all()

    assert df_weather.columns.names == df_weather_true.columns.names
    assert (df_weather.columns.dtypes == df_weather_true.columns.dtypes).all()
    assert (df_weather.columns == df_weather_true.columns).all()

    assert df_weather.index.names == df_weather_true.index.names
    assert (df_weather.index.dtypes == df_weather_true.index.dtypes).all()  # type: ignore
    assert (df_weather.index == df_weather_true.index).all()


def test_get_attrs() -> None:
    attrs = get_attrs(spec)
    keys = list(attrs.keys())
    values = list(attrs.values())

    assert keys[0] == spec.fields.of_attr[0].name
    assert keys[1] == spec.fields.of_attr[1].name
    assert keys[2] == spec.fields.of_attr[2].name

    assert values[0] == spec.fields.of_attr[0].default
    assert values[1] == spec.fields.of_attr[1].default
    assert values[2] == spec.fields.of_attr[2].default


def test_get_columns() -> None:
    columns = cast(pd.Index, get_columns(spec))

    assert columns.names[0] == spec.fields.of_column[0].name
    assert columns.names[1] == spec.fields.of_column[1].name

    assert columns[0] == spec.fields.of_data[0].name
    assert columns[1] == spec.fields.of_data[1].name
    assert columns[2] == spec.fields.of_data[2].name
    assert columns[3] == spec.fields.of_data[3].name


def test_get_data() -> None:
    data = get_data(spec)
    keys = list(data.keys())
    values = list(data.values())

    assert keys[0] == spec.fields.of_data[0].name
    assert keys[1] == spec.fields.of_data[1].name
    assert keys[2] == spec.fields.of_data[2].name
    assert keys[3] == spec.fields.of_data[3].name

    assert values[0].dtype.name == spec.fields.of_data[0].dtype
    assert values[1].dtype.name == spec.fields.of_data[1].dtype
    assert values[2].dtype.name == spec.fields.of_data[2].dtype
    assert values[3].dtype.name == spec.fields.of_data[3].dtype

    assert (values[0] == spec.fields.of_data[0].default).all()
    assert (values[1] == spec.fields.of_data[1].default).all()
    assert (values[2] == spec.fields.of_data[2].default).all()
    assert (values[3] == spec.fields.of_data[3].default).all()


def test_get_index() -> None:
    index = cast(pd.Index, get_index(spec))

    assert index.names[0] == spec.fields.of_index[0].name
    assert index.names[1] == spec.fields.of_index[1].name

    assert index.get_level_values(0).dtype == spec.fields.of_index[0].dtype
    assert index.get_level_values(1).dtype == spec.fields.of_index[1].dtype

    assert (index.get_level_values(0) == spec.fields.of_index[0].default).all()
    assert (index.get_level_values(1) == spec.fields.of_index[1].default).all()