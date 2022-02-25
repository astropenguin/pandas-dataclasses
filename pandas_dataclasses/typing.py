__all__ = []


# standard library
from enum import Enum
from typing import Hashable, TypeVar
from typing import Collection as Collection_


# dependencies
from typing_extensions import Protocol


# type hints (private)
Tdtype = TypeVar("Tdtype", covariant=True)
Tname = TypeVar("Tname", bound=Hashable, covariant=True)


class Named(Protocol[Tname]):
    pass


class Collection(Collection_[Tdtype], Named[Tname], Protocol):
    pass


# constants
class FieldType(Enum):
    DATA = "data"
    INDEX = "index"
