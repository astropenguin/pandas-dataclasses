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
    """Class property decorator dedicated to ``As.new``."""

    def __init__(self, func: Callable[..., Any]) -> None:
        self.__doc__ = func.__doc__
        self.func = func

    def __get__(
        self,
        obj: Any,
        cls: Type[PandasClass[P, TPandas]],
    ) -> Callable[P, TPandas]:
        return self.func(cls)  # type: ignore


class As(Generic[TPandas]):
    """Mix-in class that provides shorthand methods."""

    __pandas_factory__: Callable[..., TPandas]
    """Factory for pandas data creation."""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Add a pandas factory to an inheriting class."""
        cls.__pandas_factory__ = kwargs.pop("factory", get_factory(cls))
        super().__init_subclass__(**kwargs)

    @classproperty
    def new(cls) -> MethodType:
        """Create a pandas object from dataclass parameters."""
        return MethodType(get_new(cls), cls)


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


def get_new(cls: Any) -> Callable[..., Any]:
    """Create a runtime new function from a class."""
    factory = cls.__pandas_factory__
    origin = get_origin(factory) or factory

    if issubclass(origin, pd.DataFrame):
        converter: Any = asdataframe
    elif issubclass(origin, pd.Series):
        converter = asseries
    else:
        raise TypeError("Could not choose a converter.")

    @wraps(cls.__init__, "new", factory)
    def wrapper(cls: Any, *args: Any, **kwargs: Any) -> Any:
        return converter(cls(*args, **kwargs))

    return wrapper


def wraps(func: Any, name: str, return_: Any) -> Callable[[T], T]:
    """functools.wraps with modifiable name and return type."""
    if not isinstance(func, FunctionType):
        return wraps_(func)

    copied = type(func)(
        func.__code__,
        func.__globals__,
        name,
        func.__defaults__,
        func.__closure__,
    )

    for attr in (
        "__annotations__",
        "__dict__",
        "__doc__",
        "__kwdefaults__",
        "__module__",
        "__name__",
        "__qualname__",
    ):
        setattr(copied, attr, copy(getattr(func, attr)))

    copied.__annotations__["return"] = return_
    return wraps_(copied)
