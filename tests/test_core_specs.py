# standard library
from dataclasses import MISSING


# dependencies
from pandas_dataclasses import Spec, Tag
from .data import Weather, name, weather


# test data
spec = Spec.from_dataclass(Weather)
spec_updated = spec @ weather


# test functions
def test_year() -> None:
    field = spec.fields.of(Tag.INDEX)[0]

    assert field.id == "year"
    assert field.tags == (Tag.INDEX,)
    assert field.name == "Year"
    assert field.dtype == "int64"
    assert field.default is MISSING


def test_year_updated() -> None:
    field = spec_updated.fields.of(Tag.INDEX)[0]

    assert field.id == "year"
    assert field.tags == (Tag.INDEX,)
    assert field.name == "Year"
    assert field.dtype == "int64"
    assert field.default == weather.year


def test_month() -> None:
    field = spec.fields.of(Tag.INDEX)[1]

    assert field.id == "month"
    assert field.tags == (Tag.INDEX,)
    assert field.name == "Month"
    assert field.dtype == "int64"
    assert field.default is MISSING


def test_month_updated() -> None:
    field = spec_updated.fields.of(Tag.INDEX)[1]

    assert field.id == "month"
    assert field.tags == (Tag.INDEX,)
    assert field.name == "Month"
    assert field.dtype == "int64"
    assert field.default == weather.month


def test_temp_avg() -> None:
    field = spec.fields.of(Tag.DATA)[0]

    assert field.id == "temp_avg"
    assert field.tags == (Tag.DATA,)
    assert field.name == name("Temperature ({.temp_unit})", "Average")
    assert field.dtype == "float64"
    assert field.default is MISSING


def test_temp_avg_updated() -> None:
    field = spec_updated.fields.of(Tag.DATA)[0]

    assert field.id == "temp_avg"
    assert field.tags == (Tag.DATA,)
    assert field.name == name("Temperature (deg C)", "Average")
    assert field.dtype == "float64"
    assert field.default == weather.temp_avg


def test_temp_max() -> None:
    field = spec.fields.of(Tag.DATA)[1]

    assert field.id == "temp_max"
    assert field.tags == (Tag.DATA,)
    assert field.name == name("Temperature ({.temp_unit})", "Maximum")
    assert field.dtype == "float64"
    assert field.default is MISSING


def test_temp_max_updated() -> None:
    field = spec_updated.fields.of(Tag.DATA)[1]

    assert field.id == "temp_max"
    assert field.tags == (Tag.DATA,)
    assert field.name == name("Temperature (deg C)", "Maximum")
    assert field.dtype == "float64"
    assert field.default == weather.temp_max


def test_wind_avg() -> None:
    field = spec.fields.of(Tag.DATA)[2]

    assert field.id == "wind_avg"
    assert field.tags == (Tag.DATA,)
    assert field.name == name("Wind speed ({.wind_unit})", "Average")
    assert field.dtype == "float64"
    assert field.default is MISSING


def test_wind_avg_updated() -> None:
    field = spec_updated.fields.of(Tag.DATA)[2]

    assert field.id == "wind_avg"
    assert field.tags == (Tag.DATA,)
    assert field.name == name("Wind speed (m/s)", "Average")
    assert field.dtype == "float64"
    assert field.default == weather.wind_avg


def test_wind_max() -> None:
    field = spec.fields.of(Tag.DATA)[3]

    assert field.id == "wind_max"
    assert field.tags == (Tag.DATA,)
    assert field.name == name("Wind speed ({.wind_unit})", "Maximum")
    assert field.dtype == "float64"
    assert field.default is MISSING


def test_wind_max_updated() -> None:
    field = spec_updated.fields.of(Tag.DATA)[3]

    assert field.id == "wind_max"
    assert field.tags == (Tag.DATA,)
    assert field.name == name("Wind speed (m/s)", "Maximum")
    assert field.dtype == "float64"
    assert field.default == weather.wind_max


def test_loc() -> None:
    field = spec.fields.of(Tag.ATTR)[0]

    assert field.id == "loc"
    assert field.tags == (Tag.ATTR,)
    assert field.name == "Location"
    assert field.default == Weather.loc


def test_loc_updated() -> None:
    field = spec_updated.fields.of(Tag.ATTR)[0]

    assert field.id == "loc"
    assert field.tags == (Tag.ATTR,)
    assert field.name == "Location"
    assert field.default == weather.loc


def test_lon() -> None:
    field = spec.fields.of(Tag.ATTR)[1]

    assert field.id == "lon"
    assert field.tags == (Tag.ATTR,)
    assert field.name == "Longitude ({.lon_unit})"
    assert field.default == Weather.lon


def test_lon_updated() -> None:
    field = spec_updated.fields.of(Tag.ATTR)[1]

    assert field.id == "lon"
    assert field.tags == (Tag.ATTR,)
    assert field.name == "Longitude (deg)"
    assert field.default == weather.lon


def test_lat() -> None:
    field = spec.fields.of(Tag.ATTR)[2]

    assert field.id == "lat"
    assert field.tags == (Tag.ATTR,)
    assert field.name == "Latitude ({.lat_unit})"
    assert field.default == Weather.lat


def test_lat_updated() -> None:
    field = spec_updated.fields.of(Tag.ATTR)[2]

    assert field.id == "lat"
    assert field.tags == (Tag.ATTR,)
    assert field.name == "Latitude (deg)"
    assert field.default == weather.lat


def test_attrs() -> None:
    field = spec.fields.of(Tag.ATTR)[3]

    assert field.id == "attrs"
    assert field.tags == (Tag.ATTR, Tag.MULTIPLE)
    assert field.name == "attrs"
    assert field.default is MISSING


def test_attrs_updated() -> None:
    field = spec_updated.fields.of(Tag.ATTR)[3]

    assert field.id == "attrs"
    assert field.tags == (Tag.ATTR, Tag.MULTIPLE)
    assert field.name == "attrs"
    assert field.default == weather.attrs


def test_factory() -> None:
    assert spec.factory is None


def test_name() -> None:
    assert spec.name == Weather.__name__


def test_origin() -> None:
    assert spec.origin is Weather
