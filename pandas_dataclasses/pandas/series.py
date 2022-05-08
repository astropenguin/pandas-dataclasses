__all__ = ["AsSeries", "asseries"]


# standard library
from functools import wraps
from types import MethodType
from typing import Any, Callable, Type


# dependencies
import pandas as pd
from morecopy import copy
from typing_extensions import ParamSpec, Protocol


# submodules
from ..core import get_attrs, get_data, get_index, get_name
from ..typing import DataClass


# type hints
PInit = ParamSpec("PInit")


class DataClass(DataClass, Protocol[PInit]):
    """Type hint for dataclass objects (with parameter specification)."""

    def __init__(self, *args: PInit.args, **kwargs: PInit.kwargs) -> None:
        ...


# runtime classes
class classproperty:
    """Class property only for AsSeries.new().

    As ``classmethod`` and ``property`` can be chained since Python 3.9,
    this will be removed when the support for Python 3.7 and 3.8 ends.

    """

    def __init__(self, func: Any) -> None:
        self.__func__ = func

    def __get__(
        self,
        obj: Any,
        cls: Type[DataClass[PInit]],
    ) -> Callable[PInit, pd.Series]:
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
def asseries(obj: DataClass[PInit]) -> pd.Series:
    """Create a Series object from a dataclass object."""
    attrs = get_attrs(obj)
    data = get_data(obj)
    index = get_index(obj)
    name = get_name(obj)

    if data is not None:
        data = next(iter(data.values()))

    series = pd.Series(data, index, name=name)
    series.attrs.update(attrs)
    return series
