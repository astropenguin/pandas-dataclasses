__all__ = ["asdataframe", "asseries"]


# standard library
from typing import Any, Dict, Hashable, Iterable, Optional, Type, TypeVar, overload


# dependencies
import numpy as np
import pandas as pd


# submodules
from .specs import Spec
from .typing import P, T, AnyDType, AnyPandas, DataClass, PandasClass


# type hints
AnyDict = Dict[Hashable, Any]
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
    attrs = get_attrs(obj)
    data = get_data(obj)
    index = get_index(obj)
    columns = get_columns(obj)

    if factory is None:
        factory = get_factory(obj) or pd.DataFrame

    if not issubclass(factory, pd.DataFrame):
        raise TypeError("Factory was not a subclass of DataFrame.")

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
    attrs = get_attrs(obj)
    data = get_data(obj)
    index = get_index(obj)

    if data is None:
        name = None
    else:
        name = first(data.keys())
        data = first(data.values())

    if factory is None:
        factory = get_factory(obj) or pd.Series

    if not issubclass(factory, pd.Series):
        raise TypeError("Factory was not a subclass of Series.")

    series = factory(data, index, name=name)
    series.attrs.update(attrs)
    return series


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


def first(obj: Iterable[T]) -> T:
    """Return the first item of an iterable."""
    return next(iter(obj))


def get_attrs(obj: DataClass[P]) -> AnyDict:
    """Derive attributes from a dataclass object."""
    spec = Spec.from_dataclass(type(obj)).update(obj)
    attrs: AnyDict = {}

    for field in spec.fields.of_attr:
        attrs[field.hashable_name] = getattr(obj, field.id)

    return attrs


def get_columns(obj: DataClass[P]) -> Optional[pd.Index]:
    """Derive columns from a dataclass object."""
    spec = Spec.from_dataclass(type(obj)).update(obj)
    names: Any = [field.name for field in spec.fields.of_data]

    if all(isinstance(name, Hashable) for name in names):
        return

    if (
        all(isinstance(name, dict) for name in names)
        and len(set(map(tuple, names))) == 1
    ):
        return pd.MultiIndex.from_tuples(
            [tuple(name.values()) for name in names],
            names=first(names).keys(),
        )

    raise ValueError("Could not create columns.")


def get_data(obj: DataClass[P]) -> Optional[AnyDict]:
    """Derive data from a dataclass object."""
    spec = Spec.from_dataclass(type(obj)).update(obj)
    data: AnyDict = {}

    if not spec.fields.of_data:
        return

    for field in spec.fields.of_data:
        data[field.hashable_name] = astype(
            atleast_1d(getattr(obj, field.id)),
            field.dtype,
        )

    return data


def get_factory(obj: DataClass[P]) -> Optional[Type[AnyPandas]]:
    """Derive pandas factory from a dataclass object."""
    return Spec.from_dataclass(type(obj)).factory


def get_index(obj: DataClass[P]) -> Optional[pd.Index]:
    """Derive index from a dataclass object."""
    spec = Spec.from_dataclass(type(obj)).update(obj)
    indexes: AnyDict = {}

    if not spec.fields.of_index:
        return

    for field in spec.fields.of_index:
        indexes[field.hashable_name] = astype(
            atleast_1d(getattr(obj, field.id)),
            field.dtype,
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
