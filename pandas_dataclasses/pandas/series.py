__all__ = ["AsSeries", "asseries"]


# standard library
from functools import wraps
from types import MethodType
from typing import Any, Callable, Dict, Hashable, List, Optional, Type


# dependencies
import numpy as np
import pandas as pd
from morecopy import copy
from typing_extensions import ParamSpec, Protocol


# submodules
from ..specs import DataSpec
from ..typing import AnyDType, DataClass


# type hints
PInit = ParamSpec("PInit")


class DataClass(DataClass, Protocol[PInit]):
    """Type hint for dataclass objects (with parameter specification)."""

    def __init__(self, *args: PInit.args, **kwargs: PInit.kwargs) -> None:
        ...


# runtime classes
class classproperty:
    """Class property only for AsSeries.new().

    As ``classmethod`` and ``property`` can be chained since Python 3.9,
    this will be removed when the support for Python 3.7 and 3.8 ends.

    """

    def __init__(self, func: Any) -> None:
        self.__func__ = func

    def __get__(
        self,
        obj: Any,
        cls: Type[DataClass[PInit]],
    ) -> Callable[PInit, pd.Series]:
        return self.__func__(cls)


class AsSeries:
    """Mix-in class that provides shorthand methods."""

    @classproperty
    def new(cls) -> Any:
        """Create a Series object from dataclass parameters."""
        init = copy(cls.__init__)
        init.__annotations__["return"] = pd.Series

        @wraps(init)
        def new(cls: Any, *args: Any, **kwargs: Any) -> Any:
            return asseries(cls(*args, **kwargs))

        return MethodType(new, cls)


# runtime functions
def asseries(obj: DataClass[PInit]) -> pd.Series:
    """Create a Series object from a dataclass object."""
    data = get_data(obj)
    dtype = get_dtype(obj)
    index = get_index(obj)
    name = get_name(obj)

    if (
        data is not None
        and not isinstance(data, pd.Series)
        and index is not None
        and len(index) == 1
    ):
        index = index.repeat(len(data))

    series = pd.Series(data, index, dtype, name)
    series.attrs.update(get_attrs(obj))
    return series


def atleast_1d(data: Any) -> Any:
    """Convert data to be at least one dimensional."""
    return data if np.ndim(data) else [data]


def get_attrs(obj: DataClass[PInit]) -> Dict[Hashable, Any]:
    """Return the attributes for a Series object."""
    dataspec = DataSpec.from_dataclass(type(obj))
    attrs: Dict[Hashable, Any] = {}

    for key, spec in dataspec.fields.of_attr.items():
        attrs[spec.name] = getattr(obj, key)

    return attrs


def get_data(obj: DataClass[PInit]) -> Optional[Any]:
    """Return the data for a Series object."""
    dataspec = DataSpec.from_dataclass(type(obj))

    for key in dataspec.fields.of_data.keys():
        return atleast_1d(getattr(obj, key))


def get_dtype(obj: DataClass[PInit]) -> Optional[AnyDType]:
    """Return the data type (dtype) for a Series object."""
    dataspec = DataSpec.from_dataclass(type(obj))

    for spec in dataspec.fields.of_data.values():
        return spec.data.type


def get_index(obj: DataClass[PInit]) -> Optional[pd.Index]:
    """Return the (multi-level) index for a Series object."""
    dataspec = DataSpec.from_dataclass(type(obj))
    indexes: List[pd.Index] = []

    for key, spec in dataspec.fields.of_index.items():
        indexes.append(
            pd.Index(
                atleast_1d(getattr(obj, key)),
                dtype=spec.data.type,
                name=spec.name,
            )
        )

    if len(indexes) == 0:
        return

    if len(indexes) == 1:
        return indexes[0]

    repeats = max(map(len, indexes))

    for i, index in enumerate(indexes):
        if len(index) == 1:
            indexes[i] = index.repeat(repeats)

    return pd.MultiIndex.from_arrays(indexes)


def get_name(obj: DataClass[PInit]) -> Optional[Hashable]:
    """Return the name for a Series object."""
    dataspec = DataSpec.from_dataclass(type(obj))

    for key in dataspec.fields.of_name.keys():
        return getattr(obj, key)

    for spec in dataspec.fields.of_data.values():
        return spec.name
