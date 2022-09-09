__all__ = ["asdataframe", "asseries"]


# standard library
from typing import Any, Hashable, List, Optional, Type, TypeVar, overload


# dependencies
import numpy as np
import pandas as pd


# submodules
from .specs import Spec
from .typing import P, DataClass, PandasClass


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
    names = get_columns(spec)

    if factory is None:
        factory = spec.factory or pd.DataFrame

    if not issubclass(factory, pd.DataFrame):
        raise TypeError("Factory must be a subclass of DataFrame.")

    dataframe = factory(data, index)
    dataframe.columns.names = names
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


def ensure(data: Any, dtype: Optional[str]) -> Any:
    """Ensure data to be 1D and have given data type."""
    if not np.ndim(data):
        data = [data]

    if isinstance(data, (pd.Index, pd.Series)):
        return type(data)(data, dtype=dtype, copy=False)
    else:
        return pd.array(data, dtype=dtype, copy=False)


def get_attrs(spec: Spec) -> "dict[Hashable, Any]":
    """Derive attributes from a specification."""
    objs: "dict[Hashable, Any]" = {}

    for field in spec.fields.of_attr:
        objs[field.name] = field.default

    return objs


def get_columns(spec: Spec) -> "list[Hashable]":
    """Derive column names from a specification."""
    objs: "dict[Hashable, Any]" = {}

    for field in spec.fields.of_column:
        objs[field.name] = field.default

    if not objs:
        return [None]
    else:
        return list(objs.keys())


def get_data(spec: Spec) -> Optional["dict[Hashable, Any]"]:
    """Derive data from a specification."""
    objs: "dict[Hashable, Any]" = {}

    for field in spec.fields.of_data:
        objs[field.name] = ensure(field.default, field.dtype)

    return objs if objs else None


def get_index(spec: Spec) -> Optional[pd.Index]:
    """Derive index from a specification."""
    if not spec.fields.of_index:
        return

    names: List[Hashable] = []
    indexes: List[Any] = []

    for field in spec.fields.of_index:
        names.append(field.name)
        indexes.append(ensure(field.default, field.dtype))

    indexes = np.broadcast_arrays(*indexes)

    if len(indexes) == 1:
        return pd.Index(indexes[0], name=names[0])
    else:
        return pd.MultiIndex.from_arrays(indexes, names=names)
