__all__ = ["AsDataFrame"]


# standard library
from functools import wraps
from types import MethodType
from typing import Any, Callable, Type, TypeVar, overload


# dependencies
import pandas as pd
from morecopy import copy


# submodules
from .parsers import asdataframe
from .typing import P, DataClass, PandasClass


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
