__all__ = ["Attr", "Data", "Index", "Multiple"]


# standard library
from typing import Annotated, Collection


# dependencies
from ..core.tagging import Tag
from ..core.typing import TAny


# type hints
Attr = Annotated[TAny, Tag.ATTR]
"""Type hint for attribute fields (``Attr[TAny]``)."""

Data = Annotated[Collection[Annotated[TAny, Tag.DTYPE]], Tag.DATA]
"""Type hint for data fields (``Data[TAny]``)."""

Index = Annotated[Collection[Annotated[TAny, Tag.DTYPE]], Tag.INDEX]
"""Type hint for index fields (``Index[TAny]``)."""

Multiple = dict[str, Annotated[TAny, Tag.MULTIPLE]]
"""Type hint for multiple-item fields (``Multiple[TAny]``)."""
