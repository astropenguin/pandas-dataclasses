__all__ = ["Attr", "Column", "Data", "Index", "Multiple"]


# standard library
from typing import Collection, Dict, TypeVar


# dependencies
from typing_extensions import Annotated
from ..core.typing import Tag


# type hints
T = TypeVar("T")


Attr = Annotated[T, Tag.ATTR]
"""Type hint for attribute fields (``Attr[T]``)."""

Column = Annotated[T, Tag.COLUMN]
"""Type hint for column fields (``Column[T]``)."""

Data = Annotated[Collection[Annotated[T, Tag.DTYPE]], Tag.DATA]
"""Type hint for data fields (``Data[T]``)."""

Index = Annotated[Collection[Annotated[T, Tag.DTYPE]], Tag.INDEX]
"""Type hint for index fields (``Index[T]``)."""

Multiple = Dict[str, Annotated[T, Tag.MULTIPLE]]
"""Type hint for multiple-item fields (``Multiple[T]``)."""
