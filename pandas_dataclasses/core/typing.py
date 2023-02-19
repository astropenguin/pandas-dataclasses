# standard library
from dataclasses import Field
from typing import Any, Callable, Dict, Protocol, TypeVar, Union


# dependencies
from pandas import DataFrame, Series
from typing_extensions import ParamSpec


# type hints
Pandas = Union[DataFrame, "Series[Any]"]
PAny = ParamSpec("PAny")
TAny = TypeVar("TAny")
TPandas = TypeVar("TPandas", bound=Pandas)
TFrame = TypeVar("TFrame", bound=DataFrame)
TSeries = TypeVar("TSeries", bound="Series[Any]")


class DataClass(Protocol[PAny]):
    """Type hint for dataclass objects."""

    __dataclass_fields__: Dict[str, "Field[Any]"]

    def __init__(self, *args: PAny.args, **kwargs: PAny.kwargs) -> None:
        ...


class PandasClass(Protocol[PAny, TPandas]):
    """Type hint for dataclass objects with a pandas factory."""

    __dataclass_fields__: Dict[str, "Field[Any]"]
    __pandas_factory__: Callable[..., TPandas]

    def __init__(self, *args: PAny.args, **kwargs: PAny.kwargs) -> None:
        ...
