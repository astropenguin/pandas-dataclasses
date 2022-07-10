__all__ = ["get_attrs", "get_data", "get_factory", "get_index", "get_name"]


# standard library
from typing import Any, Dict, Hashable, Iterable, Optional, Type


# dependencies
import numpy as np
import pandas as pd


# submodules
from .specs import DataSpec
from .typing import AnyDType, AnyName, AnyPandas, DataClass, P, T


# type hints
AnyDict = Dict[Hashable, Any]


# runtime functions
def astype(data: Any, dtype: Optional[AnyDType]) -> Any:
    """Convert data to have given data type."""
    if dtype is None:
        return data
    else:
        return data.astype(dtype, copy=False)


def atleast_1d(data: Any) -> Any:
    """Convert data to be at least one dimensional."""
    if isinstance(data, pd.Series):
        return data
    else:
        return np.atleast_1d(data)


def final(name: AnyName) -> Hashable:
    """Return the final hashable from a name."""
    if isinstance(name, dict):
        return tuple(name.values())
    else:
        return name


def first(obj: Iterable[T]) -> T:
    """Return the first item of an iterable."""
    return next(iter(obj))


def get_attrs(obj: DataClass[P]) -> AnyDict:
    """Derive attributes from a dataclass object."""
    specs = DataSpec.from_dataclass(type(obj)).specs
    attrs: AnyDict = {}

    for key, spec in specs.of_attr.items():
        attrs[final(spec.name)] = getattr(obj, key)

    return attrs


def get_data(obj: DataClass[P]) -> Optional[AnyDict]:
    """Derive data from a dataclass object."""
    specs = DataSpec.from_dataclass(type(obj)).specs
    data: AnyDict = {}

    if not specs.of_data:
        return

    for key, spec in specs.of_data.items():
        data[final(spec.name)] = astype(
            atleast_1d(getattr(obj, key)),
            spec.dtype,
        )

    return data


def get_factory(obj: DataClass[P]) -> Optional[Type[AnyPandas]]:
    """Derive pandas factory from a dataclass object."""
    return DataSpec.from_dataclass(type(obj)).factory


def get_index(obj: DataClass[P]) -> Optional[pd.Index]:
    """Derive index from a dataclass object."""
    specs = DataSpec.from_dataclass(type(obj)).specs
    indexes: AnyDict = {}

    if not specs.of_index:
        return

    for key, spec in specs.of_index.items():
        indexes[final(spec.name)] = astype(
            atleast_1d(getattr(obj, key)),
            spec.dtype,
        )

    if len(indexes) == 1:
        return pd.Index(
            first(indexes.values()),
            name=first(indexes.keys()),
        )
    else:
        return pd.MultiIndex.from_arrays(
            np.broadcast_arrays(*indexes.values()),
            names=indexes.keys(),
        )


def get_name(obj: DataClass[P]) -> Hashable:
    """Derive name from a dataclass object."""
    specs = DataSpec.from_dataclass(type(obj)).specs

    for key in specs.of_name.keys():
        return getattr(obj, key)

    for spec in specs.of_data.values():
        return final(spec.name)
