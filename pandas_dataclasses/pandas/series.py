__all__ = ["AsSeries", "asseries"]


# standard library
from functools import wraps
from types import MethodType
from typing import Any, Callable, Type, TypeVar, overload


# dependencies
import pandas as pd
from morecopy import copy


# submodules
from ..core import get_attrs, get_data, get_factory, get_index, get_name
from ..typing import DataClass, P, PandasClass


# type hints
TSeries = TypeVar("TSeries", bound=pd.Series)


# runtime classes
class classproperty:
    """Class property only for AsSeries.new().

    As ``classmethod`` and ``property`` can be chained since Python 3.9,
    this will be removed when the support for Python 3.7 and 3.8 ends.

    """

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
        init = copy(cls.__init__)
        init.__annotations__["return"] = pd.Series

        @wraps(init)
        def new(cls: Any, *args: Any, **kwargs: Any) -> Any:
            return asseries(cls(*args, **kwargs))

        return MethodType(new, cls)


# runtime functions
@overload
def asseries(obj: Any, *, factory: Type[TSeries]) -> TSeries:
    ...


@overload
def asseries(obj: PandasClass[P, TSeries], *, factory: None = None) -> TSeries:
    ...


@overload
def asseries(obj: DataClass[P], *, factory: None = None) -> pd.Series:
    ...


def asseries(obj: Any, *, factory: Any = None) -> Any:
    """Create a Series object from a dataclass object."""
    attrs = get_attrs(obj)
    data = get_data(obj)
    index = get_index(obj)
    name = get_name(obj)

    if data is not None:
        data = next(iter(data.values()))

    if factory is None:
        factory = get_factory(obj) or pd.Series

    if not issubclass(factory, pd.Series):
        raise TypeError("Factory was not a subclass of Series.")

    series = factory(data, index, name=name)
    series.attrs.update(attrs)
    return series
