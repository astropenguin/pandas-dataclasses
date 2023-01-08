# standard library
from dataclasses import Field
from typing import Any, Callable, Dict, Protocol, TypeVar, Union


# dependencies
from pandas import DataFrame, Series
from typing_extensions import ParamSpec


# type hints
Pandas = Union[DataFrame, "Series[Any]"]
P = ParamSpec("P")
T = TypeVar("T")
TPandas = TypeVar("TPandas", bound=Pandas)
TFrame = TypeVar("TFrame", bound=DataFrame)
TSeries = TypeVar("TSeries", bound="Series[Any]")


class DataClass(Protocol[P]):
    """Type hint for dataclass objects."""

    __dataclass_fields__: Dict[str, "Field[Any]"]

    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        ...


class PandasClass(Protocol[P, TPandas]):
    """Type hint for dataclass objects with a pandas factory."""

    __dataclass_fields__: Dict[str, "Field[Any]"]
    __pandas_factory__: Callable[..., TPandas]

    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        ...
