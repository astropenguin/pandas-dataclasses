# standard library
from typing import cast


# dependencies
import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal
from data import Weather, weather, df_weather_true, ser_weather_true
from pandas_dataclasses import Spec, Tag, asframe, asseries
from pandas_dataclasses.core.api import (
    get_attrs,
    get_columns,
    get_data,
    get_index,
    name,
)


# test data
spec = Spec.from_dataclass(Weather) @ weather


# test functions
def test_asframe() -> None:
    assert_frame_equal(asframe(weather), df_weather_true)


def test_asseries() -> None:
    assert_series_equal(asseries(weather), ser_weather_true)


def test_get_attrs() -> None:
    attrs = get_attrs(spec)

    for i, (key, val) in enumerate(attrs.items()):
        assert key == spec.fields.of(Tag.ATTR)[i].name
        assert val == spec.fields.of(Tag.ATTR)[i].default


def test_get_columns() -> None:
    columns = cast(pd.MultiIndex, get_columns(spec))

    for i in range(len(columns)):
        assert columns[i] == name(spec.fields.of(Tag.DATA)[i])

    assert columns.names == name(spec.fields.of(Tag.DATA))  # type: ignore


def test_get_data() -> None:
    data = get_data(spec)

    for i, (key, val) in enumerate(data.items()):
        assert key == name(spec.fields.of(Tag.DATA)[i])
        assert val.dtype.name == spec.fields.of(Tag.DATA)[i].dtype
        assert (val == spec.fields.of(Tag.DATA)[i].default).all()


def test_get_index() -> None:
    index = cast(pd.MultiIndex, get_index(spec))

    for i in range(index.nlevels):
        level = index.get_level_values(i)
        assert level.name == spec.fields.of(Tag.INDEX)[i].name
        assert level.dtype.name == spec.fields.of(Tag.INDEX)[i].dtype
        assert (level == spec.fields.of(Tag.INDEX)[i].default).all()
