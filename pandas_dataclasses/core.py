__all__ = ["get_attrs", "get_data", "get_index", "get_name"]


# standard library
from typing import Any, Dict, Hashable, Optional


# submodules
import numpy as np
import pandas as pd
from .specs import DataSpec
from .typing import AnyDType, DataClass


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


def get_attrs(obj: DataClass) -> AnyDict:
    """Derive attributes from a dataclass object."""
    dataspec = DataSpec.from_dataclass(type(obj))
    attrs: AnyDict = {}

    for key, spec in dataspec.fields.of_attr.items():
        attrs[spec.name] = getattr(obj, key)

    return attrs


def get_data(obj: DataClass) -> Optional[AnyDict]:
    """Derive data from a dataclass object."""
    dataspec = DataSpec.from_dataclass(type(obj))
    dataset: AnyDict = {}

    for key, spec in dataspec.fields.of_data.items():
        dataset[spec.name] = astype(
            atleast_1d(getattr(obj, key)),
            spec.data.type,
        )

    if len(dataset) == 0:
        return

    return dataset


def get_index(obj: DataClass) -> Optional[pd.Index]:
    """Derive index from a dataclass object."""
    dataspec = DataSpec.from_dataclass(type(obj))
    dataset: AnyDict = {}

    for key, spec in dataspec.fields.of_index.items():
        dataset[spec.name] = astype(
            atleast_1d(getattr(obj, key)),
            spec.data.type,
        )

    if len(dataset) == 0:
        return

    if len(dataset) == 1:
        return pd.Index(
            next(iter(dataset.values())),
            name=next(iter(dataset.keys())),
        )
    else:
        return pd.MultiIndex.from_arrays(
            np.broadcast_arrays(*dataset.values()),
            names=dataset.keys(),
        )


def get_name(obj: DataClass) -> Hashable:
    """Derive name from a dataclass object."""
    dataspec = DataSpec.from_dataclass(type(obj))

    for key in dataspec.fields.of_name.keys():
        return getattr(obj, key)

    for spec in dataspec.fields.of_data.values():
        return spec.name
