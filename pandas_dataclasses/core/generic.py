__all__ = ["As", "AsDataFrame", "AsSeries"]


# standard library
from functools import wraps
from types import MethodType
from typing import Any, Callable, Generic, Type, TypeVar


# dependencies
import pandas as pd
from morecopy import copy
from typing_extensions import get_args, get_origin


# submodules
from .parsers import asdataframe, asseries
from .typing import AnyPandas, P, PandasClass


# type hints
TPandas = TypeVar("TPandas", bound=AnyPandas)


# runtime classes
class classproperty:
    """Create a pandas object from dataclass parameters."""

    def __init__(self, func: Any) -> None:
        self.__func__ = func

    def __get__(
        self,
        obj: Any,
        cls: Type[PandasClass[P, TPandas]],
    ) -> Callable[P, TPandas]:
        return self.__func__(cls)


class As(Generic[TPandas]):
    """Mix-in class that provides shorthand methods."""

    __pandas_factory__: Type[TPandas]

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Add a pandas factory to an inheriting class."""
        cls.__pandas_factory__ = get_factory(cls)
        return super().__init_subclass__(**kwargs)

    @classproperty
    def new(cls) -> Any:
        """Create a pandas object from dataclass parameters."""
        factory = cls.__pandas_factory__
        init = copy(cls.__init__)
        init.__annotations__["return"] = factory

        if issubclass(factory, pd.DataFrame):
            aspandas = asdataframe
        else:
            aspandas = asseries

        @wraps(init)
        def new(cls: Any, *args: Any, **kwargs: Any) -> Any:
            return aspandas(cls(*args, **kwargs))

        return MethodType(new, cls)


AsDataFrame = As[pd.DataFrame]
"""Alias of As[pandas.DataFrame]."""


AsSeries = As[pd.Series]
"""Alias of As[pandas.Series]."""


# runtime functions
def get_factory(cls: Any) -> Type[AnyPandas]:
    """Extract a pandas factory from an As-inherited class."""
    for base in cls.__orig_bases__:
        if get_origin(base) is not As:
            continue

        factory = get_args(base)[0]

        if issubclass(factory, (pd.DataFrame, pd.Series)):
            return factory

    raise TypeError("Could not find any pandas factory.")
