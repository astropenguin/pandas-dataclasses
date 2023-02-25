__all__ = ["asframe", "aspandas", "asseries"]


# standard library
from types import FunctionType
from typing import Any, Callable, Dict, Hashable, Iterable, Optional, Tuple, overload


# dependencies
import numpy as np
import pandas as pd
from pandas.api.types import is_list_like
from typing_extensions import get_origin
from .specs import Field, Fields, Spec
from .tagging import Tag
from .typing import DataClass, DataClassOf, PAny, TFrame, TPandas, TSeries


@overload
def aspandas(obj: DataClassOf[TPandas, PAny], *, factory: None = None) -> TPandas:
    ...


@overload
def aspandas(obj: DataClass[PAny], *, factory: Callable[..., TPandas]) -> TPandas:
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
def asframe(obj: DataClassOf[TFrame, PAny], *, factory: None = None) -> TFrame:
    ...


@overload
def asframe(obj: DataClass[PAny], *, factory: Callable[..., TFrame]) -> TFrame:
    ...


@overload
def asframe(obj: DataClass[PAny], *, factory: None = None) -> pd.DataFrame:
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
def asseries(obj: DataClassOf[TSeries, PAny], *, factory: None = None) -> TSeries:
    ...


@overload
def asseries(obj: DataClass[PAny], *, factory: Callable[..., TSeries]) -> TSeries:
    ...


@overload
def asseries(obj: DataClass[PAny], *, factory: None = None) -> "pd.Series[Any]":
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
    data: Dict[Hashable, Any] = {}

    for field in spec.fields.of(Tag.ATTR):
        data.update(items(field))

    return data


def get_columns(spec: Spec) -> Optional[pd.Index]:
    """Derive columns from a specification."""
    if not (fields := spec.fields.of(Tag.DATA)):
        return None

    if (names := name(fields)) is None:
        return None

    return squeeze(
        pd.MultiIndex.from_tuples(
            map(name, fields),
            names=names,
        )
    )


def get_data(spec: Spec) -> Dict[Hashable, Any]:
    """Derive data from a specification."""
    data: Dict[Hashable, Any] = {}

    for field in spec.fields.of(Tag.DATA):
        for key, val in items(field):
            data[key] = ensure(val, field.dtype)

    return data


def get_index(spec: Spec) -> Optional[pd.Index]:
    """Derive index from a specification."""
    if not (fields := spec.fields.of(Tag.INDEX)):
        return None

    data: Dict[Hashable, Any] = {}

    for field in fields:
        for key, val in items(field):
            data[key] = ensure(val, field.dtype)

    return squeeze(
        pd.MultiIndex.from_arrays(
            np.broadcast_arrays(*data.values()),
            names=data.keys(),
        )
    )


def items(field: Field) -> Iterable[Tuple[Hashable, Any]]:
    """Generate default(s) of a field specification."""
    if field.has(Tag.MULTIPLE):
        yield from field.default.items()
    else:
        yield (name(field), field.default)


@overload
def name(fields: Field) -> Hashable:
    ...


@overload
def name(fields: Fields) -> Optional[Hashable]:
    ...


def name(fields: Any) -> Any:
    """Derive name of a field(s) specification."""
    if isinstance(fields, Field):
        if isinstance(name := fields.name, dict):
            return tuple(name.values())
        else:
            return name

    if isinstance(fields, Fields):
        for field in fields:
            if isinstance(name := field.name, dict):
                return tuple(name.keys())


def squeeze(index: pd.Index) -> pd.Index:
    """Convert a MultiIndex to an Index if possible."""
    if index.nlevels == 1:
        return index.get_level_values(0)
    else:
        return index
