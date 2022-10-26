# standard library
from typing import cast


# dependencies
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal
from data import Weather, weather, df_weather_true, ser_weather_true
from pandas_dataclasses import Spec, asdataframe, asseries
from pandas_dataclasses.core.aspandas import get_attrs, get_columns, get_data, get_index


# test data
spec = Spec.from_dataclass(Weather) @ weather


# test functions
def test_asseries() -> None:
    assert_series_equal(asseries(weather), ser_weather_true)


def test_asdataframe() -> None:
    assert_frame_equal(asdataframe(weather), df_weather_true)


def test_get_attrs() -> None:
    attrs = get_attrs(spec)

    for i, (key, val) in enumerate(attrs.items()):
        assert key == spec.fields.of_attr[i].name
        assert val == spec.fields.of_attr[i].default


def test_get_columns() -> None:
    columns = cast(pd.Index, get_columns(spec))

    for i in range(len(columns)):
        assert columns[i] == spec.fields.of_data[i].name

    for i in range(columns.nlevels):
        assert columns.names[i] == spec.fields.of_column[i].name


def test_get_data() -> None:
    data = get_data(spec)

    for i, (key, val) in enumerate(data.items()):
        assert key == spec.fields.of_data[i].name
        assert val.dtype.name == spec.fields.of_data[i].dtype
        assert (val == spec.fields.of_data[i].default).all()


def test_get_index() -> None:
    index = cast(pd.Index, get_index(spec))

    for i in range(index.nlevels):
        level = index.get_level_values(i)
        assert level.name == spec.fields.of_index[i].name
        assert level.dtype.name == spec.fields.of_index[i].dtype
        assert (level == spec.fields.of_index[i].default).all()
