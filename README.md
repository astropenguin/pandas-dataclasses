# pandas-dataclasses

![Version](https://img.shields.io/pypi/v/pandas-dataclasses?label=Version&color=cornflowerblue&style=flat-square)
![Python](https://img.shields.io/pypi/pyversions/pandas-dataclasses?label=Python&color=cornflowerblue&style=flat-square)
![Downloads](https://img.shields.io/pypi/dm/pandas-dataclasses?label=Downloads&color=cornflowerblue&style=flat-square)
![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.6127352-cornflowerblue?style=flat-square)
![Tests](https://img.shields.io/github/workflow/status/astropenguin/pandas-dataclasses/Tests?label=Tests&style=flat-square)

pandas extension for typed Series and DataFrame creation

## Overview

pandas-dataclass makes it easy to create [pandas] Series and DataFrame objects that are "typed" (i.e. fixed data types, attributes, and names) using [dataclass]:

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
    humid: Data[float]


df = Weather.new(
    [2020, 2020, 2021, 2021, 2022],
    [1, 7, 1, 7, 1],
    [7.1, 24.3, 5.4, 25.9, 4.9],
    [65, 89, 57, 83, 52],
)
```

```plaintext
            temp  humid
year month
2020 1       7.1   65.0
     7      24.3   89.0
2021 1       5.4   57.0
     7      25.9   83.0
2022 1       4.9   52.0
```

### Features

- Type casting to [NumPy] and [pandas] data types
- Easy hierarchial indexing (`MultiIndex`)
- Metadata storing in attributes (`attrs`)
- Support for dataclass features (`field`, `__post_init__`, ...)
- Support for static type check ([Pylance], [Pyright], ...)

### Installation

```bash
pip install pandas-dataclasses
```

## How it works

pandas-dataclasses provides you the following features:

- Type hints for dataclass fields (`Attr`, `Data`, `Index`, `Name`) for specifying field types and data types
- Mix-in classes for dataclasses (`AsDataFrame`, `AsSeries`) for creating a Series or DataFrame object via a classmethod (`new`)

When you call `new`, it will first create a dataclass object and then create a Series or DataFrame object from the dataclass object according the type hints and values in it.
In the example above, `df = Weather.new(...)` is thus equivalent to:

```python
obj = Weather([2020, ...], [1, ...], [7.1, ...], [65, ...])
df = asdataframe(obj)
```

where `asdataframe` is a conversion function (you can actually use it).
pandas-dataclasses does not touch the dataclass object creation itself; this allows you to fully customize your dataclass before conversion using the dataclass features (`field`, `__post_init__`, ...).

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
    humid: Data[float]


df = Weather.new(...)
```

where fields typed by `Index` are "index fields" each value of which will become an index or a part of a hierarchial index of a DataFrame object.
Fields typed by `Data` are "data fields" each value of which will become a data column of a DataFrame object.
Fields typed by other types are just ignored in DataFrame creation.

Each data or index will be cast to the data type specified in the type hint like `Index[int]`.
Use `Any` or `None` if you do not want type casting.
See "[data typing rules](#data-typing-rules)" for more examples.

By default, field name (i.e. argument name) is used for the name of data or index.
See "[custom data/index naming](#custom-naming)" if you want to customize it.

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
class Temperature(AsSeries):
    """Temperature information."""

    year: Index[int]
    month: Index[int]
    temp: Data[float]


ser = Temperature.new(...)
```

Unlike `AsDataFrame`, the second and subsequent data fields are ignored in Series creation.
Other rules are the same as for the DataFrame creation.

## Advanced usage

### Metadata storing

Fields typed by `Attr` are "attribute fields" each value of which will become an item of attributes (`attrs`) of a DataFrame of Series object:

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
    humid: Data[float]
    loc: Attr[str] = "Tokyo"
    lon: Attr[float] = 139.69167
    lat: Attr[float] = 35.68944
```

In this example, `Weather.new(...).attrs` will become like:

```python
{"loc": "Tokyo", "lon": 139.69167, "lat": 35.68944}
```

### Custom naming

The name of data, index, or attribute can be explicitly specified by adding an annotation to the `Data`/`Index`/`Attr` type:

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
    humid: Ann[Data[float], "Humidity (%)"]
    loc: Ann[Attr[str], "Location"] = "Tokyo"
    lon: Ann[Attr[float], "Longitude (deg)"] = 139.69167
    lat: Ann[Attr[float], "Latitude (deg)"] = 35.68944
```

In this example, `Weather.new(...)` and its attributes will become like:

```plaintext
            Temperature (deg C)  Humidity (%)
Year Month
2020 1                      7.1          65.0
     7                     24.3          89.0
2021 1                      5.4          57.0
     7                     25.9          83.0
2022 1                      4.9          52.0
```

```python
{"Location": "Tokyo", "Longitude (deg)": 139.69167, "Latitude (deg)": 35.68944}
```

For the Series creation, a field typed by `Name` is a "name field" whose value will become the name of a Series object.
This is useful for dynamic naming.
See also [naming rules](#naming-rules) for more details and examples.

## Appendix

### Data typing rules

The data type (dtype) of data/index is inferred from the first `Data`/`Index` type of the corresponding field.
The following table shows how the data type is inferred:

<details>
<summary>Click to see all imports</summary>

```python
from typing import Any
from typing import Annotated as Ann
from typing import Literal as L
from pandas_dataclasses import Data
```
</details>

Type hint | Inferred data type
--- | ---
`Data[Any]` | None (no type casting)
`Data[None]` | None (no type casting)
`Data[int]` | `numpy.dtype("i8")`
`Data[numpy.int32]` | `numpy.dtype("i4")`
`Data[L["datetime64[ns]"]]` | `numpy.dtype("<M8[ns]")`
`Data[L["category"]]` | `pandas.CategoricalDtype()`
`Data[int] \| str` | `numpy.dtype("i8")`
`Data[int] \| Data[float]` | `numpy.dtype("i8")`
`Ann[Data[int], "spam"]` | `numpy.dtype("i8")`
`Data[Ann[int, "spam"]]` | `numpy.dtype("i8")`

### Naming rules

The name of data/index is determined by the following rules:

1. If a name field exists, its value will be preferentially used (Series creation only)
1. If a data/index field is annotated, the first hashable annotation in the first `Data`/`Index` type will be used
1. Otherwise, the field name (i.e. argument name) will be used

The following table shows how the name is inferred in the case of 2 and 3:

<details>
<summary>Click to see all imports</summary>

```python
from typing import Any
from typing import Annotated as Ann
from pandas_dataclasses import Data
```
</details>

Type hint | Inferred name
--- | ---
`Data[Any]` | (field name)
`Ann[Data[Any], {}]` | (field name)
`Ann[Data[Any], "spam"]` | `"spam"`
`Ann[Data[Any], "spam"]` | `"spam"`
`Ann[Data[Any], "spam", "ham"]` | `"spam"`
`Ann[Data[Any], {}, "spam"]` | `"spam"`
`Ann[Data[Any], "spam"] \| Ann[str, "ham"]` | `"spam"`
`Ann[Data[Any], "spam"] \| Ann[Data[float], "ham"]` | `"spam"`

### Development roadmap

Release version | Features
--- | ---
v0.3.0 | Support for custom factory for DataArray or Dataset creation
v0.4.0 | Support for hierarchial column
v1.0.0 | Initial major release (freezing public features until v2.0.0)

<!-- References -->
[dataclass]: https://docs.python.org/3/library/dataclasses.html
[NumPy]: https://numpy.org
[pandas]: https://pandas.pydata.org
[Pylance]: https://github.com/microsoft/pylance-release
[Pyright]: https://github.com/microsoft/pyright
