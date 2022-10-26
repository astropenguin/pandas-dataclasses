__all__ = ["As", "AsFrame", "AsSeries"]


# standard library
from copy import copy
from functools import lru_cache, wraps as wraps_
from types import FunctionType, MethodType
from typing import Any, Callable, ForwardRef, Generic, Type, Union


# dependencies
import pandas as pd
from typing_extensions import get_args, get_origin


# submodules
from .aspandas import asframe, asseries
from .typing import P, T, Pandas, PandasClass, TPandas


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
    """Mix-in class for runtime pandas data creation."""

    __pandas_factory__: Callable[..., TPandas]
    """Factory for pandas data creation."""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Add a pandas factory to an inheriting class."""
        factory = kwargs.pop("factory", None)
        cls.__pandas_factory__ = factory or get_factory(cls)
        super().__init_subclass__(**kwargs)

    @classproperty
    def new(cls) -> MethodType:
        """Runtime pandas data creator as a classmethod."""
        return MethodType(get_creator(cls), cls)


AsFrame = As[pd.DataFrame]
"""Alias of ``As[pandas.DataFrame]``."""


AsSeries = As["pd.Series[Any]"]
"""Alias of ``As[pandas.Series[Any]]``."""


@lru_cache(maxsize=None)
def get_creator(cls: Any) -> Callable[..., Pandas]:
    """Create a runtime pandas data creator."""
    factory = cls.__pandas_factory__

    if isinstance(factory, FunctionType):
        return_ = factory.__annotations__["return"]
    else:
        return_ = factory

    origin = get_origin(return_) or return_

    if issubclass(origin, pd.DataFrame):
        converter: Any = asframe
    elif issubclass(origin, pd.Series):
        converter = asseries
    else:
        raise TypeError("Could not choose a converter.")

    @wraps(cls.__init__, "new", get_return(cls))
    def wrapper(cls: Any, *args: Any, **kwargs: Any) -> Any:
        return converter(cls(*args, **kwargs))

    return wrapper


def get_factory(cls: Any) -> Callable[..., Any]:
    """Extract a pandas factory from a class."""
    return_ = get_return(cls)

    if not isinstance(return_, str):
        return return_

    # special handling for AsSeries
    if return_ == "pd.Series[Any]":
        return pd.Series

    raise TypeError("Return type must be evaluated.")


def get_return(cls: Any) -> Union[Type[Any], str]:
    """Extract a return type from a class."""
    for base in getattr(cls, "__orig_bases__", ()):
        if get_origin(base) is not As:
            continue

        tp = get_args(base)[0]

        if isinstance(tp, ForwardRef):
            return tp.__forward_arg__
        else:
            return tp  # type: ignore

    raise TypeError("Could not find any return type.")


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
