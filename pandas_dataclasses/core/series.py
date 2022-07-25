__all__ = ["AsSeries"]


# standard library
from functools import wraps
from types import MethodType
from typing import Any, Callable, Type, TypeVar, overload


# dependencies
import pandas as pd
from morecopy import copy


# submodules
from .parsers import asseries
from .typing import P, DataClass, PandasClass


# type hints
TSeries = TypeVar("TSeries", bound=pd.Series)


# runtime classes
class classproperty:
    """Create a Series object from dataclass parameters."""

    def __init__(self, func: Any) -> None:
        self.__func__ = func

    @overload
    def __get__(
        self,
        obj: Any,
        cls: Type[PandasClass[P, TSeries]],
    ) -> Callable[P, TSeries]:
        ...

    @overload
    def __get__(
        self,
        obj: Any,
        cls: Type[DataClass[P]],
    ) -> Callable[P, pd.Series]:
        ...

    def __get__(self, obj: Any, cls: Any) -> Any:
        return self.__func__(cls)


class AsSeries:
    """Mix-in class that provides shorthand methods."""

    @classproperty
    def new(cls) -> Any:
        """Create a Series object from dataclass parameters."""
        factory = getattr(cls, "__pandas_factory__", pd.Series)
        init = copy(cls.__init__)
        init.__annotations__["return"] = factory

        @wraps(init)
        def new(cls: Any, *args: Any, **kwargs: Any) -> Any:
            return asseries(cls(*args, **kwargs))

        return MethodType(new, cls)
