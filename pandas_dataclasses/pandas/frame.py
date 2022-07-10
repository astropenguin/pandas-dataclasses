__all__ = ["AsDataFrame", "asdataframe"]


# standard library
from functools import wraps
from types import MethodType
from typing import Any, Callable, Type, TypeVar, overload


# dependencies
import pandas as pd
from morecopy import copy


# submodules
from ..parsers import get_attrs, get_columns, get_data, get_factory, get_index
from ..typing import DataClass, P, PandasClass


# type hints
TDataFrame = TypeVar("TDataFrame", bound=pd.DataFrame)


# runtime classes
class classproperty:
    """Create a DataFrame object from dataclass parameters."""

    def __init__(self, func: Any) -> None:
        self.__func__ = func

    @overload
    def __get__(
        self,
        obj: Any,
        cls: Type[PandasClass[P, TDataFrame]],
    ) -> Callable[P, TDataFrame]:
        ...

    @overload
    def __get__(
        self,
        obj: Any,
        cls: Type[DataClass[P]],
    ) -> Callable[P, pd.DataFrame]:
        ...

    def __get__(self, obj: Any, cls: Any) -> Any:
        return self.__func__(cls)


class AsDataFrame:
    """Mix-in class that provides shorthand methods."""

    @classproperty
    def new(cls) -> Any:
        """Create a DataFrame object from dataclass parameters."""
        factory = getattr(cls, "__pandas_factory__", pd.DataFrame)
        init = copy(cls.__init__)
        init.__annotations__["return"] = factory

        @wraps(init)
        def new(cls: Any, *args: Any, **kwargs: Any) -> Any:
            return asdataframe(cls(*args, **kwargs))

        return MethodType(new, cls)


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
