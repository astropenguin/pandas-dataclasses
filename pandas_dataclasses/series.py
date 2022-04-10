__all__ = ["asseries"]


# standard library
from typing import Any, Dict, Hashable, List, Optional, Union


# dependencies
import numpy as np
import pandas as pd
from typing_extensions import ParamSpec, Protocol


# submodules
from .dataspec import DataSpec
from .typing import DataClass


# type hints
IndexLike = Union[List[pd.Index], pd.Index]
PInit = ParamSpec("PInit")


class DataClass(DataClass, Protocol[PInit]):
    """Type hint for dataclass objects (with parameter specification)."""

    def __init__(self, *args: PInit.args, **kwargs: PInit.kwargs) -> None:
        ...


# runtime functions
def asseries(obj: DataClass[PInit]) -> "pd.Series[Any]":
    """Create a Series object from a pandas dataclass."""
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


def get_dtype(obj: DataClass[PInit]) -> Optional["np.dtype[Any]"]:
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
