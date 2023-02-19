__all__ = ["Attr", "Column", "Data", "Index", "Multiple"]


# standard library
from typing import Collection, Dict


# dependencies
from typing_extensions import Annotated
from ..core.tagging import Tag
from ..core.typing import TAny


# type hints
Attr = Annotated[TAny, Tag.ATTR]
"""Type hint for attribute fields (``Attr[TAny]``)."""

Column = Annotated[TAny, Tag.COLUMN]
"""Type hint for column fields (``Column[TAny]``)."""

Data = Annotated[Collection[Annotated[TAny, Tag.DTYPE]], Tag.DATA]
"""Type hint for data fields (``Data[TAny]``)."""

Index = Annotated[Collection[Annotated[TAny, Tag.DTYPE]], Tag.INDEX]
"""Type hint for index fields (``Index[TAny]``)."""

Multiple = Dict[str, Annotated[TAny, Tag.MULTIPLE]]
"""Type hint for multiple-item fields (``Multiple[TAny]``)."""
