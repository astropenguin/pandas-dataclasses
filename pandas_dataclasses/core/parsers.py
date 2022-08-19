__all__ = ["asdataframe", "asseries"]


# standard library
from typing import Any, Hashable, List, Optional, Type, TypeVar, overload


# dependencies
import numpy as np
import pandas as pd


# submodules
from .specs import Spec
from .typing import P, AnyDType, DataClass, PandasClass


# type hints
TDataFrame = TypeVar("TDataFrame", bound=pd.DataFrame)
TSeries = TypeVar("TSeries", bound=pd.Series)


# runtime functions
@overload
def asdataframe(obj: Any, *, factory: Type[TDataFrame]) -> TDataFrame:
    ...


@overload
def asdataframe(obj: PandasClass[P, TDataFrame], *, factory: None = None) -> TDataFrame:
    ...


@overload
def asdataframe(obj: DataClass[P], *, factory: None = None) -> pd.DataFrame:
    ...


def asdataframe(obj: Any, *, factory: Any = None) -> Any:
    """Create a DataFrame object from a dataclass object."""
    spec = Spec.from_dataclass(type(obj)) @ obj
    attrs = get_attrs(spec)
    data = get_data(spec)
    index = get_index(spec)
    columns = get_columns(spec)

    if factory is None:
        factory = spec.factory or pd.DataFrame

    if not issubclass(factory, pd.DataFrame):
        raise TypeError("Factory must be a subclass of DataFrame.")

    dataframe = factory(data, index, columns)
    dataframe.attrs.update(attrs)
    return dataframe


@overload
def asseries(obj: Any, *, factory: Type[TSeries]) -> TSeries:
    ...


@overload
def asseries(obj: PandasClass[P, TSeries], *, factory: None = None) -> TSeries:
    ...


@overload
def asseries(obj: DataClass[P], *, factory: None = None) -> pd.Series:
    ...


def asseries(obj: Any, *, factory: Any = None) -> Any:
    """Create a Series object from a dataclass object."""
    spec = Spec.from_dataclass(type(obj)) @ obj
    attrs = get_attrs(spec)
    data = get_data(spec)
    index = get_index(spec)

    if data is None:
        name = None
    else:
        name, data = list(data.items())[0]

    if factory is None:
        factory = spec.factory or pd.Series

    if not issubclass(factory, pd.Series):
        raise TypeError("Factory must be a subclass of Series.")

    series = factory(data, index, name=name)
    series.attrs.update(attrs)
    return series


def ensure(data: Any, dtype: Optional[AnyDType]) -> Any:
    """Ensure data to be 1D and have given data type."""
    if not isinstance(data, (pd.Index, pd.Series)):
        data = np.atleast_1d(data)

    if dtype is None:
        return data
    else:
        return data.astype(dtype, copy=False)


def get_attrs(spec: Spec) -> "dict[Hashable, Any]":
    """Derive attributes from a specification."""
    attrs: "dict[Hashable, Any]" = {}

    for field in spec.fields.of_attr:
        attrs[field.hashable_name] = field.default

    return attrs


def get_columns(spec: Spec) -> Optional[pd.Index]:
    """Derive columns from a specification."""
    if not spec.fields.of_data:
        return

    names_ = [field.name for field in spec.fields.of_data]

    if all(isinstance(name, Hashable) for name in names_):
        return

    if not all(isinstance(name, dict) for name in names_):
        raise ValueError("All names must be dictionaries.")

    names = [tuple(name.keys()) for name in names_]  # type: ignore
    indexes = [tuple(name.values()) for name in names_]  # type: ignore

    if not len(set(names)) == 1:
        raise ValueError("All name keys must be same.")

    return pd.MultiIndex.from_tuples(indexes, names=names[0])


def get_data(spec: Spec) -> Optional["dict[Hashable, Any]"]:
    """Derive data from a specification."""
    if not spec.fields.of_data:
        return

    names: List[Hashable] = []
    data: List[Any] = []

    for field in spec.fields.of_data:
        names.append(field.hashable_name)
        data.append(ensure(field.default, field.dtype))

    return dict(zip(names, data))


def get_index(spec: Spec) -> Optional[pd.Index]:
    """Derive index from a specification."""
    if not spec.fields.of_index:
        return

    names: List[Hashable] = []
    indexes: List[Any] = []

    for field in spec.fields.of_index:
        names.append(field.hashable_name)
        indexes.append(ensure(field.default, field.dtype))

    indexes = np.broadcast_arrays(*indexes)

    if len(indexes) == 1:
        return pd.Index(indexes[0], name=names[0])
    else:
        return pd.MultiIndex.from_arrays(indexes, names=names)
