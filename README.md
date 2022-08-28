# pandas-dataclasses

[![Release](https://img.shields.io/pypi/v/pandas-dataclasses?label=Release&color=cornflowerblue&style=flat-square)](https://pypi.org/project/pandas-dataclasses/)
[![Python](https://img.shields.io/pypi/pyversions/pandas-dataclasses?label=Python&color=cornflowerblue&style=flat-square)](https://pypi.org/project/pandas-dataclasses/)
[![Downloads](https://img.shields.io/pypi/dm/pandas-dataclasses?label=Downloads&color=cornflowerblue&style=flat-square)](https://pepy.tech/project/pandas-dataclasses)
[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.6127352-cornflowerblue?style=flat-square)](https://doi.org/10.5281/zenodo.6127352)
[![Tests](https://img.shields.io/github/workflow/status/astropenguin/pandas-dataclasses/Tests?label=Tests&style=flat-square)](https://github.com/astropenguin/pandas-dataclasses/actions)

pandas data creation made easy by dataclass

## Overview

pandas-dataclass makes it easy to create [pandas] data (Series and DataFrame) by Python's [dataclass] that enables to specify their data types, attributes, and names:

<details>
<summary>Click to see all imports</summary>

```python
from dataclasses import dataclass
from pandas_dataclasses import AsDataFrame, Data, Index
```
</details>

```python
@dataclass
class Weather(AsDataFrame):
    """Weather information."""

    year: Index[int]
    month: Index[int]
    temp: Data[float]
    wind: Data[float]


df = Weather.new(
    [2020, 2020, 2021, 2021, 2022],
    [1, 7, 1, 7, 1],
    [7.1, 24.3, 5.4, 25.9, 4.9],
    [2.4, 3.1, 2.3, 2.4, 2.6],
)
```

where `df` will become a DataFrame object like:

```
            temp  wind
year month
2020 1       7.1   2.4
     7      24.3   3.1
2021 1       5.4   2.3
     7      25.9   2.4
2022 1       4.9   2.6
```

### Features

- Type specification of pandas indexes and data
- Metadata storing in pandas data attributes
- Support for hierarchical index and columns
- Support for full [dataclass] features
- Support for static type check by [Pyright] ([Pylance])

### Installation

```bash
pip install pandas-dataclasses
```

## How it works

pandas-dataclasses provides you the following features:

- Type hints for dataclass fields (`Attr`, `Data`, `Index`) to specify index(es), data, and attributes of pandas data
- Mix-in classes for dataclasses (`As`, `AsDataFrame`, `AsSeries`) to create pandas data by a classmethod (`new`) that takes the same arguments as dataclass initialization

When you call `new`, it will first create a dataclass object and then create a Series or DataFrame object from the dataclass object according the type hints and values in it.
In the example above, `df = Weather.new(...)` is thus equivalent to:

```python
obj = Weather([2020, ...], [1, ...], [7.1, ...], [2.4, ...])
df = asdataframe(obj)
```

where `asdataframe` is a conversion function.
pandas-dataclasses does not touch the dataclass object creation itself; this allows you to fully customize your dataclass before conversion by the dataclass features (`field`, `__post_init__`, ...).

## Basic usage

### DataFrame creation

As shown in the example above, a dataclass that has the `AsDataFrame` mix-in will create DataFrame objects:

<details>
<summary>Click to see all imports</summary>

```python
from dataclasses import dataclass
from pandas_dataclasses import AsDataFrame, Data, Index
```
</details>

```python
@dataclass
class Weather(AsDataFrame):
    """Weather information."""

    year: Index[int]
    month: Index[int]
    temp: Data[float]
    wind: Data[float]


df = Weather.new(...)
```

where fields typed by `Index` are "index fields", each value of which will become an index or a part of a hierarchical index of a DataFrame object.
Fields typed by `Data` are "data fields", each value of which will become a data column of a DataFrame object.
Fields typed by other types are just ignored in the DataFrame creation.

Each data or index will be cast to the data type specified in a type hint like `Index[int]`.
Use `Any` or `None` (like `Index[Any]`) if you do not want type casting.
See also [data typing rules](#data-typing-rules) for more examples.

By default, a field name (i.e. an argument name) is used for the name of corresponding data or index.
See also [custom naming](#custom-naming) and [naming rules](#naming-rules) if you want customization.

### Series creation

A dataclass that has the `AsSeries` mix-in will create Series objects:

<details>
<summary>Click to see all imports</summary>

```python
from dataclasses import dataclass
from pandas_dataclasses import AsSeries, Data, Index
```
</details>

```python
@dataclass
class Weather(AsSeries):
    """Weather information."""

    year: Index[int]
    month: Index[int]
    temp: Data[float]


ser = Weather.new(...)
```

Unlike `AsDataFrame`, the second and subsequent data fields are ignored in the Series creation even if they exist.
Other rules are the same as for the DataFrame creation.

## Advanced usage

### Metadata storing

Fields typed by `Attr` are "attribute fields", each value of which will become an item of attributes of a DataFrame or a Series object:

<details>
<summary>Click to see all imports</summary>

```python
from dataclasses import dataclass
from pandas_dataclasses import AsDataFrame, Attr, Data, Index
```
</details>

```python
@dataclass
class Weather(AsDataFrame):
    """Weather information."""

    year: Index[int]
    month: Index[int]
    temp: Data[float]
    wind: Data[float]
    loc: Attr[str] = "Tokyo"
    lon: Attr[float] = 139.69167
    lat: Attr[float] = 35.68944


df = Weather.new(...)
```

where `df.attrs` will become like:

```python
{"loc": "Tokyo", "lon": 139.69167, "lat": 35.68944}
```

### Custom naming

The name of data, index, or attribute can be explicitly specified by adding a hashable annotation to the corresponding type:

<details>
<summary>Click to see all imports</summary>

```python
from dataclasses import dataclass
from typing import Annotated as Ann
from pandas_dataclasses import AsDataFrame, Attr, Data, Index
```
</details>

```python
@dataclass
class Weather(AsDataFrame):
    """Weather information."""

    year: Ann[Index[int], "Year"]
    month: Ann[Index[int], "Month"]
    temp: Ann[Data[float], "Temperature (deg C)"]
    wind: Ann[Data[float], "Wind speed (m/s)"]
    loc: Ann[Attr[str], "Location"] = "Tokyo"
    lon: Ann[Attr[float], "Longitude (deg)"] = 139.69167
    lat: Ann[Attr[float], "Latitude (deg)"] = 35.68944


df = Weather.new(...)
```

where `df` and `df.attrs` will become like:

```
            Temperature (deg C)  Wind speed (m/s)
Year Month
2020 1                      7.1               2.4
     7                     24.3               3.1
2021 1                      5.4               2.3
     7                     25.9               2.4
2022 1                      4.9               2.6
```

```python
{"Location": "Tokyo", "Longitude (deg)": 139.69167, "Latitude (deg)": 35.68944}
```

Adding dictionary annotations to data fields will create DataFrame objects with hierarchical columns, where dictionary keys will become the names of column levels and dictionary values will become the names of columns:

<details>
<summary>Click to see all imports</summary>

```python
from dataclasses import dataclass
from typing import Annotated as Ann
from pandas_dataclasses import AsDataFrame, Data, Index
```
</details>

```python
def name(stat: str, cat: str) -> dict[str, str]:
    return {"Statistic": stat, "Category": cat}


@dataclass
class Weather(AsDataFrame):
    """Weather information."""

    year: Ann[Index[int], "Year"]
    month: Ann[Index[int], "Month"]
    temp_avg: Ann[Data[float], name("Temperature (deg C)", "Average")]
    temp_max: Ann[Data[float], name("Temperature (deg C)", "Maximum")]
    wind_avg: Ann[Data[float], name("Wind speed (m/s)", "Average")]
    wind_max: Ann[Data[float], name("Wind speed (m/s)", "Maximum")]


df = Weather.new(...)
```

where `df` will become like:

```
Statistic  Temperature (deg C)        Wind speed (m/s)
Category              Average Maximum          Average Maximum
Year Month
2020 1                    7.1    11.1              2.4     8.8
     7                   24.3    27.7              3.1    10.2
2021 1                    5.4    10.3              2.3    10.7
     7                   25.9    30.3              2.4     9.0
2022 1                    4.9     9.4              2.6     8.8
```

If an annotation is a [format string] or a dictionary that has [format string]s as keys and/or values, it will be formatted by a dataclass object before the data creation:

<details>
<summary>Click to see all imports</summary>

```python
from dataclasses import dataclass
from typing import Annotated as Ann
from pandas_dataclasses import AsDataFrame, Data, Index
```
</details>

```python
@dataclass
class Weather(AsDataFrame):
    """Weather information."""

    year: Ann[Index[int], "Year"]
    month: Ann[Index[int], "Month"]
    temp: Ann[Data[float], "Temperature ({.temp_unit})"]
    wind: Ann[Data[float], "Wind speed ({.wind_unit})"]
    temp_unit: str = "deg C"
    wind_unit: str = "m/s"
```

where units of the temperature and the wind speed can be dynamically updated like `Weather.new(..., temp_unit="deg F", wind_unit="km/h"`).

### Custom pandas factory

A custom class can be specified as a factory for the Series or DataFrame creation by `As`, the generic version of `AsDataFrame` and `AsSeries`.
Note that the custom class must be a subclass of either `pandas.Series` or `pandas.DataFrame`:

<details>
<summary>Click to see all imports</summary>

```python
import pandas as pd
from dataclasses import dataclass
from pandas_dataclasses import As, Data, Index
```
</details>

```python
class CustomSeries(pd.Series):
    """Custom pandas Series."""

    pass


@dataclass
class Temperature(As[CustomSeries]):
    """Temperature information."""

    year: Index[int]
    month: Index[int]
    temp: Data[float]


ser = Temperature.new(...)
```

where `ser` will be a `CustomSeries` object.

## Appendix

### Data typing rules

The data type (dtype) of data/index is determined from the first `Data`/`Index` type of the corresponding field.
The following table shows how the data type is inferred:

<details>
<summary>Click to see all imports</summary>

```python
from typing import Any, Annotated as Ann, Literal as L
from pandas_dataclasses import Data
```
</details>

Type hint | Inferred data type
--- | ---
`Data[Any]` | `None` (no type casting)
`Data[None]` | `None` (no type casting)
`Data[int]` | `numpy.int64`
`Data[numpy.int32]` | `numpy.int32`
`Data[L["datetime64[ns]"]]` | `numpy.dtype("<M8[ns]")`
`Data[L["category"]]` | `pandas.CategoricalDtype()`
`Data[int] \| str` | `numpy.int64`
`Data[int] \| Data[float]` | `numpy.int64`
`Ann[Data[int], "spam"]` | `numpy.int64`
`Data[Ann[int, "spam"]]` | `numpy.int64`

### Naming rules

The name of data/index/attribute is determined from the first annotation of the first `Data`/`Index`/`Attr` type of the corresponding field.
If the annotation is a [format string] or a dictionary that has [format string]s as keys and/or values, it will be formatted by a dataclass object before the data creation.
Otherwise, the field name (i.e. argument name) will be used.
The following table shows how the name is inferred:

<details>
<summary>Click to see all imports</summary>

```python
from typing import Any, Annotated as Ann
from pandas_dataclasses import Data
```
</details>

Type hint | Inferred name
--- | ---
`Data[Any]` | (field name)
`Ann[Data[Any], "spam"]` | `"spam"`
`Ann[Data[Any], "spam", "ham"]` | `"spam"`
`Ann[Data[Any], "spam"] \| Ann[str, "ham"]` | `"spam"`
`Ann[Data[Any], "spam"] \| Ann[Data[float], "ham"]` | `"spam"`
`Ann[Data[Any], "{.name}"` | `"{.name}".format(obj)`
`Ann[Data[Any], {"0": "spam", "1": "ham"}]` | `("spam", "ham")`
`Ann[Data[Any], {"0": "{.name}", "1": "ham"}]` | `("{.name}".format(obj), "ham")`

where `obj` is a dataclass object that is expected to have `obj.name`.

### Development roadmap

Release version | Features
--- | ---
v0.5 | Support for dynamic naming
v0.6 | support for extension array and dtype
v1.0 | Initial major release (freezing public features until v2.0)

<!-- References -->
[dataclass]: https://docs.python.org/3/library/dataclasses.html
[format string]: https://docs.python.org/3/library/string.html#format-string-syntax
[NumPy]: https://numpy.org
[pandas]: https://pandas.pydata.org
[Pylance]: https://github.com/microsoft/pylance-release
[Pyright]: https://github.com/microsoft/pyright
