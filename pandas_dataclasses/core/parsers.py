__all__ = ["asdataframe", "asseries"]


# standard library
from typing import Any, Dict, Hashable, Iterable, Optional, Type, TypeVar, overload


# dependencies
import numpy as np
import pandas as pd


# submodules
from .specs import DataSpec
from .typing import P, T, AnyDType, AnyName, AnyPandas, DataClass, PandasClass


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
    name = get_name(obj)

    if data is not None:
        data = next(iter(data.values()))

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


def get_columns(obj: DataClass[P]) -> Optional[pd.Index]:
    """Derive columns from a dataclass object."""
    specs = DataSpec.from_dataclass(type(obj)).specs
    names: Any = [spec.name for spec in specs.of_data.values()]

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
