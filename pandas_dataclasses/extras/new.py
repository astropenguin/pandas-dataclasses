__all__ = ["As", "AsFrame", "AsSeries"]


# standard library
from inspect import signature
from types import MethodType
from typing import Any, Callable, ForwardRef, Generic, Type, Union


# dependencies
import pandas as pd
from typing_extensions import get_args, get_origin
from ..core.api import aspandas
from ..core.typing import P, PandasClass, TPandas


class classproperty:
    """Class property decorator dedicated to ``As.new``."""

    def __init__(self, fget: Callable[..., Any]) -> None:
        self.fget = fget

    def __get__(
        self,
        obj: Any,
        cls: Type[PandasClass[P, TPandas]],
    ) -> Callable[P, TPandas]:
        return self.fget(cls)  # type: ignore


class As(Generic[TPandas]):
    """Pandas data creation by a classmethod (``new``)."""

    __pandas_factory__: Callable[..., TPandas]
    """Factory for pandas data creation."""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Add a pandas factory to an inheriting class."""
        factory = kwargs.pop("factory", None)
        cls.__pandas_factory__ = factory or get_factory(cls)
        super().__init_subclass__(**kwargs)

    @classproperty
    def new(cls) -> MethodType:
        """Return a classmethod for pandas data creation."""

        sig = signature(cls.__init__)  # type: ignore
        sig = sig.replace(return_annotation=get_return(cls))

        def new(cls: Any, *args: Any, **kwargs: Any) -> Any:
            """Create a pandas data from dataclass arguments."""
            return aspandas(cls(*args, **kwargs))

        setattr(new, "__signature__", sig)
        return MethodType(new, cls)


AsFrame = As[pd.DataFrame]
"""Alias of ``As[pandas.DataFrame]``."""


AsSeries = As["pd.Series[Any]"]
"""Alias of ``As[pandas.Series[Any]]``."""


def get_factory(cls: Any) -> Callable[..., Any]:
    """Extract a pandas factory from a class."""
    factory = get_return(cls)

    if callable(factory):
        return factory

    # special handling for AsSeries
    if factory == "pd.Series[Any]":
        return pd.Series

    raise TypeError("Factory must be callable.")


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
