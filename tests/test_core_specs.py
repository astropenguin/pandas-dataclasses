# standard library
from dataclasses import MISSING


# dependencies
from data import Weather, weather
from pandas_dataclasses import Spec


# test data
spec = Spec.from_dataclass(Weather)
spec_updated = spec @ weather


# test functions
def test_year() -> None:
    field = spec.fields.of_index[0]

    assert field.id == "year"
    assert field.name == "Year"
    assert field.tag == "index"
    assert field.dtype == "int64"
    assert field.default is MISSING


def test_year_updated() -> None:
    field = spec_updated.fields.of_index[0]

    assert field.id == "year"
    assert field.name == "Year"
    assert field.tag == "index"
    assert field.dtype == "int64"
    assert field.default == weather.year


def test_month() -> None:
    field = spec.fields.of_index[1]

    assert field.id == "month"
    assert field.name == "Month"
    assert field.tag == "index"
    assert field.dtype == "int64"
    assert field.default is MISSING


def test_month_updated() -> None:
    field = spec_updated.fields.of_index[1]

    assert field.id == "month"
    assert field.name == "Month"
    assert field.tag == "index"
    assert field.dtype == "int64"
    assert field.default == weather.month


def test_meas() -> None:
    field = spec.fields.of_column[0]

    assert field.id == "meas"
    assert field.name == "Measurement"
    assert field.tag == "column"
    assert field.default is MISSING


def test_meas_updated() -> None:
    field = spec_updated.fields.of_column[0]

    assert field.id == "meas"
    assert field.name == "Measurement"
    assert field.tag == "column"
    assert field.default is MISSING


def test_stat() -> None:
    field = spec.fields.of_column[1]

    assert field.id == "stat"
    assert field.name == "Statistic"
    assert field.tag == "column"
    assert field.default is MISSING


def test_stat_updated() -> None:
    field = spec_updated.fields.of_column[1]

    assert field.id == "stat"
    assert field.name == "Statistic"
    assert field.tag == "column"
    assert field.default is MISSING


def test_temp_avg() -> None:
    field = spec.fields.of_data[0]

    assert field.id == "temp_avg"
    assert field.name == ("Temperature ({.temp_unit})", "Average")
    assert field.tag == "data"
    assert field.dtype == "float64"
    assert field.default is MISSING


def test_temp_avg_updated() -> None:
    field = spec_updated.fields.of_data[0]

    assert field.id == "temp_avg"
    assert field.name == ("Temperature (deg C)", "Average")
    assert field.tag == "data"
    assert field.dtype == "float64"
    assert field.default == weather.temp_avg


def test_temp_max() -> None:
    field = spec.fields.of_data[1]

    assert field.id == "temp_max"
    assert field.name == ("Temperature ({.temp_unit})", "Maximum")
    assert field.tag == "data"
    assert field.dtype == "float64"
    assert field.default is MISSING


def test_temp_max_updated() -> None:
    field = spec_updated.fields.of_data[1]

    assert field.id == "temp_max"
    assert field.name == ("Temperature (deg C)", "Maximum")
    assert field.tag == "data"
    assert field.dtype == "float64"
    assert field.default == weather.temp_max


def test_wind_avg() -> None:
    field = spec.fields.of_data[2]

    assert field.id == "wind_avg"
    assert field.name == ("Wind speed ({.wind_unit})", "Average")
    assert field.tag == "data"
    assert field.dtype == "float64"
    assert field.default is MISSING


def test_wind_avg_updated() -> None:
    field = spec_updated.fields.of_data[2]

    assert field.id == "wind_avg"
    assert field.name == ("Wind speed (m/s)", "Average")
    assert field.tag == "data"
    assert field.dtype == "float64"
    assert field.default == weather.wind_avg


def test_wind_max() -> None:
    field = spec.fields.of_data[3]

    assert field.id == "wind_max"
    assert field.name == ("Wind speed ({.wind_unit})", "Maximum")
    assert field.tag == "data"
    assert field.dtype == "float64"
    assert field.default is MISSING


def test_wind_max_updated() -> None:
    field = spec_updated.fields.of_data[3]

    assert field.id == "wind_max"
    assert field.name == ("Wind speed (m/s)", "Maximum")
    assert field.tag == "data"
    assert field.dtype == "float64"
    assert field.default == weather.wind_max


def test_loc() -> None:
    field = spec.fields.of_attr[0]

    assert field.id == "loc"
    assert field.name == "Location"
    assert field.tag == "attr"
    assert field.default == Weather.loc


def test_loc_updated() -> None:
    field = spec_updated.fields.of_attr[0]

    assert field.id == "loc"
    assert field.name == "Location"
    assert field.tag == "attr"
    assert field.default == weather.loc


def test_lon() -> None:
    field = spec.fields.of_attr[1]

    assert field.id == "lon"
    assert field.name == "Longitude ({.lon_unit})"
    assert field.tag == "attr"
    assert field.default == Weather.lon


def test_lon_updated() -> None:
    field = spec_updated.fields.of_attr[1]

    assert field.id == "lon"
    assert field.name == "Longitude (deg)"
    assert field.tag == "attr"
    assert field.default == weather.lon


def test_lat() -> None:
    field = spec.fields.of_attr[2]

    assert field.id == "lat"
    assert field.name == "Latitude ({.lat_unit})"
    assert field.tag == "attr"
    assert field.default == Weather.lat


def test_lat_updated() -> None:
    field = spec_updated.fields.of_attr[2]

    assert field.id == "lat"
    assert field.name == "Latitude (deg)"
    assert field.tag == "attr"
    assert field.default == weather.lat


def test_factory() -> None:
    assert spec.factory is None


def test_name() -> None:
    assert spec.name == Weather.__name__
