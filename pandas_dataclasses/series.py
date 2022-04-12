__all__ = ["AsSeries", "asseries"]


# standard library
from functools import wraps
from types import MethodType
from typing import Any, Callable, Dict, Hashable, List, Optional, Type, Union


# dependencies
import numpy as np
import pandas as pd
from morecopy import copy
from typing_extensions import ParamSpec, Protocol, TypeAlias


# submodules
from .dataspec import DataSpec
from .typing import AnyDType, DataClass


# type hints
AnySeries: TypeAlias = "pd.Series[Any]"
IndexLike = Union[List[pd.Index], pd.Index]
PInit = ParamSpec("PInit")


class DataClass(DataClass, Protocol[PInit]):
    """Type hint for dataclass objects (with parameter specification)."""

    def __init__(self, *args: PInit.args, **kwargs: PInit.kwargs) -> None:
        ...


# runtime classes
class classproperty:
    """Class property only for AsSeries.new().

    As a classmethod and a property can be chained together since Python 3.9,
    this class will be removed when the support for Python 3.7 and 3.8 ends.

    """

    def __init__(self, func: Any) -> None:
        self.__func__ = func

    def __get__(
        self,
        obj: Any,
        cls: Type[DataClass[PInit]],
    ) -> Callable[PInit, AnySeries]:
        return self.__func__(cls)


class AsSeries:
    """Mix-in class that provides shorthand methods."""

    @classproperty
    def new(cls) -> Any:
        """Create a Series object from dataclass parameters."""
        init = copy(cls.__init__)
        init.__annotations__["return"] = AnySeries

        @wraps(init)
        def new(cls: Any, *args: Any, **kwargs: Any) -> Any:
            return asseries(cls(*args, **kwargs))

        return MethodType(new, cls)


# runtime functions
def asseries(obj: DataClass[PInit]) -> AnySeries:
    """Create a Series object from a dataclass object."""
    series = pd.Series(
        data=get_data(obj),
        dtype=get_dtype(obj),
        index=get_index(obj),  # type: ignore
        name=get_name(obj),
    )

    series.attrs.update(get_attrs(obj))
    return series


def get_attrs(obj: DataClass[PInit]) -> Dict[Hashable, Any]:
    """Return the attributes for a Series object."""
    dataspec = DataSpec.from_dataclass(type(obj))
    attrs: Dict[Hashable, Any] = {}

    for key, spec in dataspec.fields.attr.items():
        attrs[spec.name] = getattr(obj, key)

    return attrs


def get_data(obj: DataClass[PInit]) -> Optional[Any]:
    """Return the data for a Series object."""
    dataspec = DataSpec.from_dataclass(type(obj))

    for key in dataspec.fields.data:
        return getattr(obj, key)


def get_dtype(obj: DataClass[PInit]) -> Optional[AnyDType]:
    """Return the data type (dtype) for a Series object."""
    dataspec = DataSpec.from_dataclass(type(obj))

    for spec in dataspec.fields.data.values():
        return spec.data.type


def get_index(obj: DataClass[PInit]) -> Optional[IndexLike]:
    """Return the index(es) for a Series object."""
    dataspec = DataSpec.from_dataclass(type(obj))
    indexes: List[pd.Index] = []

    for key, spec in dataspec.fields.index.items():
        indexes.append(
            pd.Index(
                np.atleast_1d(getattr(obj, key)),
                dtype=spec.data.type,
                name=spec.name,
            )
        )

    if len(indexes) > 1:
        return indexes

    if len(indexes) == 1:
        return indexes[0]


def get_name(obj: DataClass[PInit]) -> Optional[Hashable]:
    """Return the name for a Series object."""
    dataspec = DataSpec.from_dataclass(type(obj))

    for key in dataspec.fields.name:
        return getattr(obj, key)

    for spec in dataspec.fields.data.values():
        return spec.name
