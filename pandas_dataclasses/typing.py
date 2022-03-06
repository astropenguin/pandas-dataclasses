__all__ = ["Data", "Index", "NamedData", "NamedIndex"]


# standard library
from enum import Enum
from typing import Collection, Hashable, TypeVar, Union


# dependencies
from typing_extensions import Annotated, Protocol


# type hints (private)
TDtype = TypeVar("TDtype", covariant=True)
TName = TypeVar("TName", bound=Hashable, covariant=True)


class Named(Protocol[TName]):
    pass


class Collection(Named[TName], Collection[TDtype], Protocol):
    pass


# type hints (public)
class FieldType(Enum):
    DATA = "data"
    INDEX = "index"


Data = Annotated[Union[Collection[None, TDtype], TDtype], FieldType.DATA]
Index = Annotated[Union[Collection[None, TDtype], TDtype], FieldType.INDEX]
NamedData = Annotated[Union[Collection[TName, TDtype], TDtype], FieldType.DATA]
NamedIndex = Annotated[Union[Collection[TName, TDtype], TDtype], FieldType.INDEX]
