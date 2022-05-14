# pandas-dataclasses

![Version](https://img.shields.io/pypi/v/pandas-dataclasses?label=Version&color=cornflowerblue&style=flat-square)
![Python](https://img.shields.io/pypi/pyversions/pandas-dataclasses?label=Python&color=cornflowerblue&style=flat-square)
![Downloads](https://img.shields.io/pypi/dm/pandas-dataclasses?label=Downloads&color=cornflowerblue&style=flat-square)
![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.6127352-cornflowerblue?style=flat-square)
![Tests](https://img.shields.io/github/workflow/status/astropenguin/pandas-dataclasses/Tests?label=Tests&style=flat-square)

pandas extension for typed Series and DataFrame creation

## Overview

pandas-dataclass makes it easy to create [pandas] Series and DataFrame objects that are "typed" (i.e. fixed data types, attributes, and names) using [dataclass]:

```python
from dataclasses import dataclass
from pandas_dataclasses import AsDataFrame, Data, Index


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

- Type casting to NumPy and pandas data types
- Hierarchial indexing (`MultiIndex`)
- Metadata storing (`attrs`)
- Support for dataclass features (`field`, `__post_init__`, ...)
- Support for static type check ([Pylance], [Pyright], ...)

### Installation

```bash
pip install pandas-dataclasses
```

<!-- References -->
[dataclass]: https://docs.python.org/3/library/dataclasses.html
[pandas]: https://pandas.pydata.org
[Pylance]: https://github.com/microsoft/pylance-release
[Pyright]: https://github.com/microsoft/pyright
