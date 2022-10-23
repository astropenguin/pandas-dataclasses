__all__ = ["As", "AsDataFrame", "AsSeries"]


# standard library
from copy import copy
from functools import wraps as wraps_
from types import FunctionType, MethodType
from typing import Any, Callable, ForwardRef, Generic, Type, cast


# dependencies
import pandas as pd
from typing_extensions import get_args, get_origin


# submodules
from .asdata import asdataframe, asseries
from .typing import P, T, PandasClass, TPandas


class classproperty:
    """Class property dedicated to ``As.new``."""

    def __init__(self, func: Any) -> None:
        self.__doc__ = func.__doc__
        self.func = func

    def __get__(
        self,
        obj: Any,
        cls: Type[PandasClass[P, TPandas]],
    ) -> Callable[P, TPandas]:
        return self.func(cls)  # type: ignore


def wraps(func: Any, return_: Any) -> Callable[[T], T]:
    """Function decorator dedicated to ``As.new``."""
    if not isinstance(func, FunctionType):
        return wraps_(func)

    copied = type(func)(
        func.__code__,
        func.__globals__,
        "new",
        func.__defaults__,
        func.__closure__,
    )

    for name in (
        "__annotations__",
        "__dict__",
        "__doc__",
        "__kwdefaults__",
        "__module__",
        "__name__",
        "__qualname__",
    ):
        setattr(copied, name, copy(getattr(func, name)))

    copied.__annotations__["return"] = return_
    return wraps_(copied)


class As(Generic[TPandas]):
    """Mix-in class that provides shorthand methods."""

    __pandas_factory__: Callable[..., TPandas]
    """Factory for pandas data creation."""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Add a pandas factory to an inheriting class."""
        cls.__pandas_factory__ = kwargs.pop("factory", get_factory(cls))
        super().__init_subclass__(**kwargs)

    @classproperty
    def new(cls) -> Any:
        """Create a pandas object from dataclass parameters."""
        factory = cls.__pandas_factory__

        if issubclass(factory, pd.DataFrame):
            aspandas: Any = asdataframe
        elif issubclass(factory, pd.Series):
            aspandas = asseries
        else:
            raise TypeError("Not a valid pandas factory.")

        @wraps(cls.__init__, factory)  # type: ignore
        def new(cls: Any, *args: Any, **kwargs: Any) -> Any:
            return aspandas(cls(*args, **kwargs))

        return MethodType(new, cls)


AsDataFrame = As[pd.DataFrame]
"""Alias of ``As[pandas.DataFrame]``."""


AsSeries = As["pd.Series[Any]"]
"""Alias of ``As[pandas.Series[Any]]``."""


def get_factory(cls: Any) -> Callable[..., Any]:
    """Extract a pandas factory from a class."""
    for base in getattr(cls, "__orig_bases__", ()):
        if get_origin(base) is not As:
            continue

        factory = get_args(base)[0]

        # special handling for AsSeries
        if factory == ForwardRef("pd.Series[Any]"):
            return pd.Series

        return cast(Callable[..., Any], factory)

    raise TypeError("Could not find any factory.")

