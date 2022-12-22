__all__ = ["asframe", "aspandas", "asseries"]


# standard library
from types import FunctionType
from typing import Any, Callable, Dict, Hashable, List, Optional, overload


# dependencies
import numpy as np
import pandas as pd
from pandas.api.types import is_list_like
from typing_extensions import get_origin
from .specs import Spec
from .typing import P, DataClass, PandasClass, TFrame, TPandas, TSeries


# runtime functions
@overload
def aspandas(obj: PandasClass[P, TPandas], *, factory: None = None) -> TPandas:
    ...


@overload
def aspandas(obj: DataClass[P], *, factory: Callable[..., TPandas]) -> TPandas:
    ...


def aspandas(obj: Any, *, factory: Any = None) -> Any:
    """Create a DataFrame or Series object from a dataclass object.

    Which data structure is created will be determined by a factory
    defined as the ``__pandas_factory__`` attribute in the original
    dataclass of ``obj`` or the ``factory`` argument. If a factory is
    a function, it must have an annotation of the return type.

    Args:
        obj: Dataclass object that should have attribute, column, data,
            and/or index fields. If the original dataclass has the
            ``__pandas_factory__`` attribute, it will be used as a
            factory for the data creation.

    Keyword Args:
        factory: Class or function for the DataFrame or Series creation.
            It must take the same parameters as ``pandas.DataFrame``
            or ``pandas.Series``, and return an object of it or its
            subclass. If it is a function, it must have an annotation
            of the return type. If passed, it will be preferentially
            used even if the original dataclass of ``obj`` has the
            ``__pandas_factory__`` attribute.

    Returns:
        DataFrame or Series object that complies with the original dataclass.

    Raises:
        ValueError: Raised if no factory is found or the return type
            cannot be inferred from a factory when it is a function.

    """
    spec = Spec.from_dataclass(type(obj)) @ obj

    if factory is None:
        factory = spec.factory

    if factory is None:
        raise ValueError("Could not find any factory.")

    if isinstance(factory, FunctionType):
        return_ = factory.__annotations__["return"]
    else:
        return_ = factory

    origin = get_origin(return_) or return_

    if issubclass(origin, pd.DataFrame):
        return asframe(obj, factory=factory)
    elif issubclass(origin, pd.Series):
        return asseries(obj, factory=factory)
    else:
        raise ValueError("Could not infer an object type.")


@overload
def asframe(obj: PandasClass[P, TFrame], *, factory: None = None) -> TFrame:
    ...


@overload
def asframe(obj: DataClass[P], *, factory: Callable[..., TFrame]) -> TFrame:
    ...


@overload
def asframe(obj: DataClass[P], *, factory: None = None) -> pd.DataFrame:
    ...


def asframe(obj: Any, *, factory: Any = None) -> Any:
    """Create a DataFrame object from a dataclass object.

    The return type will be determined by a factory defined as the
    ``__pandas_factory__`` attribute in the original dataclass of
    ``obj`` or the ``factory`` argument. If neither is specified,
    it defaults to ``pandas.DataFrame``.

    Args:
        obj: Dataclass object that should have attribute, column, data,
            and/or index fields. If the original dataclass has the
            ``__pandas_factory__`` attribute, it will be used as a
            factory for the DataFrame creation.

    Keyword Args:
        factory: Class or function for the DataFrame creation.
            It must take the same parameters as ``pandas.DataFrame``,
            and return an object of it or its subclass. If passed, it
            will be preferentially used even if the original dataclass
            of ``obj`` has the ``__pandas_factory__`` attribute.

    Returns:
        DataFrame object that complies with the original dataclass.

    """
    spec = Spec.from_dataclass(type(obj)) @ obj

    if factory is None:
        factory = spec.factory or pd.DataFrame

    dataframe = factory(
        data=get_data(spec),
        index=get_index(spec),
        columns=get_columns(spec),
    )

    dataframe.attrs.update(get_attrs(spec))
    return dataframe


@overload
def asseries(obj: PandasClass[P, TSeries], *, factory: None = None) -> TSeries:
    ...


@overload
def asseries(obj: DataClass[P], *, factory: Callable[..., TSeries]) -> TSeries:
    ...


@overload
def asseries(obj: DataClass[P], *, factory: None = None) -> "pd.Series[Any]":
    ...


def asseries(obj: Any, *, factory: Any = None) -> Any:
    """Create a Series object from a dataclass object.

    The return type will be determined by a factory defined as the
    ``__pandas_factory__`` attribute in the original dataclass of
    ``obj`` or the ``factory`` argument. If neither is specified,
    it defaults to ``pandas.Series``.

    Args:
        obj: Dataclass object that should have attribute, column, data,
            and/or index fields. If the original dataclass has the
            ``__pandas_factory__`` attribute, it will be used as a
            factory for the Series creation.

    Keyword Args:
        factory: Class or function for the Series creation.
            It must take the same parameters as ``pandas.Series``,
            and return an object of it or its subclass. If passed, it
            will be preferentially used even if the original dataclass
            of ``obj`` has the ``__pandas_factory__`` attribute.

    Returns:
        Series object that complies with the original dataclass.

    """
    spec = Spec.from_dataclass(type(obj)) @ obj

    if factory is None:
        factory = spec.factory or pd.Series

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
    if not is_list_like(data):
        data = [data]

    if isinstance(data, (pd.Index, pd.Series)):
        return type(data)(data, dtype=dtype, copy=False)
    else:
        return pd.array(data, dtype=dtype, copy=False)


def get_attrs(spec: Spec) -> Dict[Hashable, Any]:
    """Derive attributes from a specification."""
    attrs: Dict[Hashable, Any] = {}

    for field in spec.fields.of_attr:
        attrs[field.name] = field.default

    return attrs


def get_columns(spec: Spec) -> Optional[pd.Index]:
    """Derive columns from a specification."""
    names = [field.name for field in spec.fields.of_column]
    elems = [field.name for field in spec.fields.of_data]

    if len(names) == 0:
        return None
    if len(names) == 1:
        return pd.Index(elems, name=names[0], tupleize_cols=False)
    else:
        return pd.MultiIndex.from_tuples(elems, names=names)


def get_data(spec: Spec) -> Dict[Hashable, Any]:
    """Derive data from a specification."""
    data: Dict[Hashable, Any] = {}

    for field in spec.fields.of_data:
        data[field.name] = ensure(field.default, field.dtype)

    return data


def get_index(spec: Spec) -> Optional[pd.Index]:
    """Derive index from a specification."""
    names: List[Hashable] = []
    elems: List[Any] = []

    for field in spec.fields.of_index:
        names.append(field.name)
        elems.append(ensure(field.default, field.dtype))

    if len(names) == 0:
        return None
    if len(names) == 1:
        return pd.Index(elems[0], name=names[0])
    else:
        elems = np.broadcast_arrays(*elems)
        return pd.MultiIndex.from_arrays(elems, names=names)
