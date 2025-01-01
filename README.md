# pandas-dataclasses

[![Release](https://img.shields.io/pypi/v/pandas-dataclasses?label=Release&color=cornflowerblue&style=flat-square)](https://pypi.org/project/pandas-dataclasses/)
[![Python](https://img.shields.io/pypi/pyversions/pandas-dataclasses?label=Python&color=cornflowerblue&style=flat-square)](https://pypi.org/project/pandas-dataclasses/)
[![Downloads](https://img.shields.io/pypi/dm/pandas-dataclasses?label=Downloads&color=cornflowerblue&style=flat-square)](https://pepy.tech/project/pandas-dataclasses)
[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.6127352-cornflowerblue?style=flat-square)](https://doi.org/10.5281/zenodo.6127352)
[![Tests](https://img.shields.io/github/actions/workflow/status/astropenguin/pandas-dataclasses/tests.yml?label=Tests&style=flat-square)](https://github.com/astropenguin/pandas-dataclasses/actions)

pandas data creation by data classes

## Overview

pandas-dataclass makes it easy to create [pandas] data (DataFrame and Series) by specifying their data types, attributes, and names using the Python's dataclass:

<details>
<summary>Click to see all imports</summary>

```python
from dataclasses import dataclass
from pandas_dataclasses import AsFrame, Data, Index
```
</details>

```python
@dataclass
class Weather(AsFrame):
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

- Specifying data types and names of each element in pandas data
- Specifying metadata stored in pandas data attributes (attrs)
- Support for hierarchical index and columns
- Support for custom factory for data creation
- Support for full [dataclass] features
- Support for static type check by [mypy] and [Pyright] ([Pylance])

### Installation

```bash
pip install pandas-dataclasses
```

## How it works

pandas-dataclasses provides you the following features:

- Type hints for dataclass fields (`Attr`, `Data`, `Index`) to specify the data type and name of each element in pandas data
- Mix-in classes for dataclasses (`As`, `AsFrame`, `AsSeries`) to create pandas data by a classmethod (`new`) that takes the same arguments as dataclass initialization

When you call `new`, it will first create a dataclass object and then create a Series or DataFrame object from the dataclass object according the type hints and values in it.
In the example above, `df = Weather.new(...)` is thus equivalent to:

<details>
<summary>Click to see all imports</summary>

```python
from pandas_dataclasses import asframe
```
</details>

```python
obj = Weather([2020, ...], [1, ...], [7.1, ...], [2.4, ...])
df = asframe(obj)
```

where `asframe` is a conversion function.
pandas-dataclasses does not touch the dataclass object creation itself; this allows you to fully customize your dataclass before conversion by the dataclass features (`field`, `__post_init__`, ...).

## Basic usage

### DataFrame creation

As shown in the example above, a dataclass that has the `AsFrame` (or `AsDataFrame` as an alias) mix-in will create DataFrame objects:

<details>
<summary>Click to see all imports</summary>

```python
from dataclasses import dataclass
from pandas_dataclasses import AsFrame, Data, Index
```
</details>

```python
@dataclass
class Weather(AsFrame):
    """Weather information."""

    year: Index[int]
    month: Index[int]
    temp: Data[float]
    wind: Data[float]


df = Weather.new(...)
```

where fields typed by `Index` are *index fields*, each value of which will become an index or a part of a hierarchical index of a DataFrame object.
Fields typed by `Data` are *data fields*, each value of which will become a data column of a DataFrame object.
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

Unlike `AsFrame`, the second and subsequent data fields are ignored in the Series creation even if they exist.
Other rules are the same as for the DataFrame creation.

## Advanced usage

### Metadata storing

Fields typed by `Attr` are *attribute fields*, each value of which will become an item of attributes of a DataFrame or a Series object:

<details>
<summary>Click to see all imports</summary>

```python
from dataclasses import dataclass
from pandas_dataclasses import AsFrame, Attr, Data, Index
```
</details>

```python
@dataclass
class Weather(AsFrame):
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

The name of attribute, data, or index can be explicitly specified by adding a hashable annotation to the corresponding type:

<details>
<summary>Click to see all imports</summary>

```python
from dataclasses import dataclass
from typing import Annotated as Ann
from pandas_dataclasses import AsFrame, Attr, Data, Index
```
</details>

```python
@dataclass
class Weather(AsFrame):
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

If an annotation is a [format string], it will be formatted by a dataclass object before the data creation:

<details>
<summary>Click to see all imports</summary>

```python
from dataclasses import dataclass
from typing import Annotated as Ann
from pandas_dataclasses import AsFrame, Data, Index
```
</details>

```python
@dataclass
class Weather(AsFrame):
    """Weather information."""

    year: Ann[Index[int], "Year"]
    month: Ann[Index[int], "Month"]
    temp: Ann[Data[float], "Temperature ({.temp_unit})"]
    wind: Ann[Data[float], "Wind speed ({.wind_unit})"]
    temp_unit: str = "deg C"
    wind_unit: str = "m/s"


df = Weather.new(..., temp_unit="deg F", wind_unit="km/h")
```

where units of the temperature and the wind speed will be dynamically updated (see also [naming rules](#naming-rules)).

### Hierarchical columns

Adding tuple annotations to data fields will create DataFrame objects with hierarchical columns:

<details>
<summary>Click to see all imports</summary>

```python
from dataclasses import dataclass
from typing import Annotated as Ann
from pandas_dataclasses import AsFrame, Data, Index
```
</details>

```python
@dataclass
class Weather(AsFrame):
    """Weather information."""

    year: Ann[Index[int], "Year"]
    month: Ann[Index[int], "Month"]
    temp_avg: Ann[Data[float], ("Temperature (deg C)", "Average")]
    temp_max: Ann[Data[float], ("Temperature (deg C)", "Maximum")]
    wind_avg: Ann[Data[float], ("Wind speed (m/s)", "Average")]
    wind_max: Ann[Data[float], ("Wind speed (m/s)", "Maximum")]


df = Weather.new(...)
```

where `df` will become like:

```
           Temperature (deg C)         Wind speed (m/s)
                       Average Maximum          Average Maximum
Year Month
2020 1                     7.1    11.1              2.4     8.8
     7                    24.3    27.7              3.1    10.2
2021 1                     5.4    10.3              2.3    10.7
     7                    25.9    30.3              2.4     9.0
2022 1                     4.9     9.4              2.6     8.8
```

Column names can be (explicitly) specified by dictionary annotations:

<details>
<summary>Click to see all imports</summary>

```python
from dataclasses import dataclass
from typing import Annotated as Ann
from pandas_dataclasses import AsFrame, Data, Index
```
</details>

```python
def name(meas: str, stat: str) -> dict[str, str]:
    """Create a dictionary annotation for a column name."""
    return {"Measurement": meas, "Statistic": stat}


@dataclass
class Weather(AsFrame):
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
Measurement Temperature (deg C)         Wind speed (m/s)
Statistic               Average Maximum          Average Maximum
Year Month
2020 1                      7.1    11.1              2.4     8.8
     7                     24.3    27.7              3.1    10.2
2021 1                      5.4    10.3              2.3    10.7
     7                     25.9    30.3              2.4     9.0
2022 1                      4.9     9.4              2.6     8.8
```

If a tuple or dictionary annotation has [format string]s, they will also be formatted by a dataclass object (see also [naming rules](#naming-rules)).

### Multiple-item fields

Multiple (and possibly extra) attributes, data, or indices can be added by fields with corresponding type hints wrapped by `Multiple`:

<details>
<summary>Click to see all imports</summary>

```python
from dataclasses import dataclass
from pandas_dataclasses import AsFrame, Data, Index, Multiple
```
</details>


```python
@dataclass
class Weather(AsFrame):
    """Weather information."""

    year: Index[int]
    month: Index[int]
    temp: Data[float]
    wind: Data[float]
    extra_index: Multiple[Index[int]]
    extra_data: Multiple[Data[float]]


df = Weather.new(
    [2020, 2020, 2021, 2021, 2022],
    [1, 7, 1, 7, 1],
    [7.1, 24.3, 5.4, 25.9, 4.9],
    [2.4, 3.1, 2.3, 2.4, 2.6],
    extra_index={
        "day": [1, 1, 1, 1, 1],
        "week": [2, 2, 4, 3, 5],
    },
    extra_data={
        "humid": [65, 89, 57, 83, 52],
        "press": [1013.8, 1006.2, 1014.1, 1007.7, 1012.7],
    },
)
```

where `df` will become like:

```
                     temp  wind  humid   press
year month day week
2020 1     1   2      7.1   2.4   65.0  1013.8
     7     1   2     24.3   3.1   89.0  1006.2
2021 1     1   4      5.4   2.3   57.0  1014.1
     7     1   3     25.9   2.4   83.0  1007.7
2022 1     1   5      4.9   2.6   52.0  1012.7
```

If multiple items of the same name exist, the last-defined one will be finally used.
For example, if the `extra_index` field contains `"month": [2, 8, 2, 8, 2]`, the values given by the `month` field will be overwritten.

### Custom pandas factory

A custom class can be specified as a factory for the Series or DataFrame creation by `As`, the generic version of `AsFrame` and `AsSeries`.
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

where `ser` is statically regarded as `CustomSeries` and will become a `CustomSeries` object.

Generic Series type (`Series[T]`) is also supported, however, it is only for static the type check in the current pandas versions.
In such cases, you can additionally give a factory that must work in runtime as a class argument:

<details>
<summary>Click to see all imports</summary>

```python
import pandas as pd
from dataclasses import dataclass
from pandas_dataclasses import As, Data, Index
```
</details>

```python
@dataclass
class Temperature(As["pd.Series[float]"], factory=pd.Series):
    """Temperature information."""

    year: Index[int]
    month: Index[int]
    temp: Data[float]


ser = Temperature.new(...)
```

where `ser` is statically regarded as `Series[float]` but will become a `Series` object in runtime.

## Appendix

### Data typing rules

The data type (dtype) of data or index is determined from the first `Data` or `Index` type of the corresponding field, respectively.
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
`Data[int \| str]` | `numpy.int64`
`Data[numpy.int32]` | `numpy.int32`
`Data[L["datetime64[ns]"]]` | `numpy.dtype("<M8[ns]")`
`Data[L["category"]]` | `pandas.CategoricalDtype()`
`Data[int] \| str` | `numpy.int64`
`Data[int] \| Data[float]` | `numpy.int64`
`Ann[Data[int], "spam"]` | `numpy.int64`
`Data[Ann[int, "spam"]]` | `numpy.int64`

### Naming rules

The name of attribute, data, or index is determined from the first annotation of the first `Attr`, `Data`, or `Index` type of the corresponding field, respectively.
If the annotation is a [format string] or a tuple that has [format string]s, it (they) will be formatted by a dataclass object before the data creation.
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
`Ann[Data[Any], ..., "spam"]` | (field name)
`Ann[Data[Any], "spam"]` | `"spam"`
`Ann[Data[Any], "spam", "ham"]` | `"spam"`
`Ann[Data[Any], "spam"] \| Ann[str, "ham"]` | `"spam"`
`Ann[Data[Any], "spam"] \| Ann[Data[float], "ham"]` | `"spam"`
`Ann[Data[Any], "{.name}"` | `"{.name}".format(obj)`
`Ann[Data[Any], ("spam", "ham")]` | `("spam", "ham")`
`Ann[Data[Any], ("{.name}", "ham")]` | `("{.name}".format(obj), "ham")`

where `obj` is a dataclass object that is expected to have `obj.name`.

### Development roadmap

Release version | Features
--- | ---
v0.5 | Support for dynamic naming
v0.6 | Support for extension array and dtype
v0.7 | Support for hierarchical columns
v0.8 | Support for mypy and callable pandas factory
v0.9 | Support for Ellipsis (`...`) as an alias of field name
v0.10 | Support for union type in type hints
v0.11 | Support for Python 3.11 and drop support for Python 3.7
v0.12 | Support for multiple items received in a single field
v1.0 | Initial major release (freezing public features until v2.0)

<!-- References -->
[dataclass]: https://docs.python.org/3/library/dataclasses.html
[format string]: https://docs.python.org/3/library/string.html#format-string-syntax
[mypy]: http://www.mypy-lang.org
[NumPy]: https://numpy.org
[pandas]: https://pandas.pydata.org
[Pylance]: https://github.com/microsoft/pylance-release
[Pyright]: https://github.com/microsoft/pyright
