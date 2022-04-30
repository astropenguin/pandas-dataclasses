__all__ = ["get_attrs", "get_data", "get_dtype", "get_index", "get_name"]


# standard library
from typing import Any, Dict, Hashable, List, Optional


# dependencies
import numpy as np
import pandas as pd


# submodules
from ..specs import DataSpec
from ..typing import AnyDType, DataClass


# runtime functions
def atleast_1d(data: Any) -> Any:
    """Convert data to be at least one dimensional."""
    return data if np.ndim(data) else [data]


def get_attrs(obj: DataClass) -> Dict[Hashable, Any]:
    """Return the attributes for a Series object."""
    dataspec = DataSpec.from_dataclass(type(obj))
    attrs: Dict[Hashable, Any] = {}

    for key, spec in dataspec.fields.of_attr.items():
        attrs[spec.name] = getattr(obj, key)

    return attrs


def get_data(obj: DataClass) -> Optional[Any]:
    """Return the data for a Series object."""
    dataspec = DataSpec.from_dataclass(type(obj))

    for key in dataspec.fields.of_data.keys():
        return atleast_1d(getattr(obj, key))


def get_dtype(obj: DataClass) -> Optional[AnyDType]:
    """Return the data type (dtype) for a Series object."""
    dataspec = DataSpec.from_dataclass(type(obj))

    for spec in dataspec.fields.of_data.values():
        return spec.data.type


def get_index(obj: DataClass) -> Optional[pd.Index]:
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


def get_name(obj: DataClass) -> Optional[Hashable]:
    """Return the name for a Series object."""
    dataspec = DataSpec.from_dataclass(type(obj))

    for key in dataspec.fields.of_name.keys():
        return getattr(obj, key)

    for spec in dataspec.fields.of_data.values():
        return spec.name
