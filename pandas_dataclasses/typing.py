__all__ = ["Data", "Index", "NamedData", "NamedIndex"]


# standard library
from enum import Enum
from typing import Hashable, TypeVar, Union
from typing import Collection as Collection_


# dependencies
from typing_extensions import Annotated, Protocol


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


# type hints (public)
Data = Annotated[Union[Collection[Tdtype, None], Tdtype], FieldType.DATA]
Index = Annotated[Union[Collection[Tdtype, None], Tdtype], FieldType.INDEX]
NamedData = Annotated[Union[Collection[Tdtype, Tname], Tdtype], FieldType.DATA]
NamedIndex = Annotated[Union[Collection[Tdtype, Tname], Tdtype], FieldType.INDEX]
