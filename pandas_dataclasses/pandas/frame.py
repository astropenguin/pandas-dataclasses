__all__ = ["AsDataFrame", "asdataframe"]


# standard library
from functools import wraps
from types import MethodType
from typing import Any, Callable, Type, TypeVar, overload


# dependencies
import pandas as pd
from morecopy import copy


# submodules
from ..core import get_attrs, get_data, get_factory, get_index
from ..typing import DataClass, P, PandasClass


# type hints
TDataFrame = TypeVar("TDataFrame", bound=pd.DataFrame)


# runtime classes
class classproperty:
    """Class property only for AsDataFrame.new().

    As ``classmethod`` and ``property`` can be chained since Python 3.9,
    this will be removed when the support for Python 3.7 and 3.8 ends.

    """

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
        init = copy(cls.__init__)
        init.__annotations__["return"] = pd.DataFrame

        @wraps(init)
        def new(cls: Any, *args: Any, **kwargs: Any) -> Any:
            return asdataframe(cls(*args, **kwargs))

        return MethodType(new, cls)


# runtime functions
@overload
def asdataframe(obj: PandasClass[P, TDataFrame], factory: None = None) -> TDataFrame:
    ...


@overload
def asdataframe(obj: DataClass[P], factory: None = None) -> pd.DataFrame:
    ...


@overload
def asdataframe(obj: Any, factory: Type[pd.DataFrame] = pd.DataFrame) -> pd.DataFrame:
    ...


def asdataframe(obj: Any, factory: Any = None) -> Any:
    """Create a DataFrame object from a dataclass object."""
    attrs = get_attrs(obj)
    data = get_data(obj)
    index = get_index(obj)

    if factory is None:
        factory = get_factory(obj) or pd.DataFrame

    if not issubclass(factory, pd.DataFrame):
        raise TypeError("Factory was not a subclass of DataFrame.")

    dataframe = factory(data, index)
    dataframe.attrs.update(attrs)
    return dataframe
