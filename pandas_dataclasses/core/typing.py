__all__ = [
    "DataClass",
    "DataClassOf",
    "Pandas",
    "PAny",
    "TAny",
    "TFrame",
    "TPandas",
    "TSeries",
]


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
TFrame = TypeVar("TFrame", bound=DataFrame)
TPandas = TypeVar("TPandas", bound=Pandas)
TSeries = TypeVar("TSeries", bound="Series[Any]")


class DataClass(Protocol[PAny]):
    """Type hint for dataclass objects."""

    __dataclass_fields__: Dict[str, "Field[Any]"]

    def __init__(self, *args: PAny.args, **kwargs: PAny.kwargs) -> None:
        ...


class DataClassOf(Protocol[TPandas, PAny]):
    """Type hint for dataclass objects with a pandas factory."""

    __dataclass_fields__: Dict[str, "Field[Any]"]
    __pandas_factory__: Callable[..., TPandas]

    def __init__(self, *args: PAny.args, **kwargs: PAny.kwargs) -> None:
        ...
