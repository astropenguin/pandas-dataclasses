__all__ = ["asdataframe", "asseries"]


# standard library
from typing import Any, Hashable, Optional, Type, overload


# dependencies
import numpy as np
import pandas as pd


# submodules
from .specs import Spec
from .typing import P, DataClass, PandasClass, TDataFrame, TSeries


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

    if factory is None:
        factory = spec.factory or pd.DataFrame

    if not issubclass(factory, pd.DataFrame):
        raise TypeError("Factory must be a subclass of DataFrame.")

    dataframe = factory(
        data=get_data(spec),
        index=get_index(spec),
        columns=get_columns(spec),
    )

    dataframe.attrs.update(get_attrs(spec))
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

    if factory is None:
        factory = spec.factory or pd.Series

    if not issubclass(factory, pd.Series):
        raise TypeError("Factory must be a subclass of Series.")

    data = get_data(spec)
    index = get_index(spec)

    if not data:
        series = factory(index=index)
    else:
        name, data = next(iter(data.items()))
        series = factory(data=data, index=index, name=name)

    series.attrs.update(get_attrs(spec))
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
    attrs: "dict[Hashable, Any]" = {}

    for field in spec.fields.of_attr:
        attrs[field.name] = field.default

    return attrs


def get_columns(spec: Spec) -> Optional[pd.Index]:
    """Derive columns from a specification."""
    names = [field.name for field in spec.fields.of_column]
    elems = [field.name for field in spec.fields.of_data]

    if len(names) == 0:
        return
    if len(names) == 1:
        return pd.Index(pd.array(elems), name=names[0])
    else:
        return pd.MultiIndex.from_tuples(elems, names=names)


def get_data(spec: Spec) -> "dict[Hashable, Any]":
    """Derive data from a specification."""
    data: "dict[Hashable, Any]" = {}

    for field in spec.fields.of_data:
        data[field.name] = ensure(field.default, field.dtype)

    return data


def get_index(spec: Spec) -> Optional[pd.Index]:
    """Derive index from a specification."""
    names: "list[Hashable]" = []
    elems: "list[Any]" = []

    for field in spec.fields.of_index:
        names.append(field.name)
        elems.append(ensure(field.default, field.dtype))

    if len(names) == 0:
        return
    if len(names) == 1:
        return pd.Index(elems[0], name=names[0])
    else:
        elems = np.broadcast_arrays(*elems)
        return pd.MultiIndex.from_arrays(elems, names=names)
