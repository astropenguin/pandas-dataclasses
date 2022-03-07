__all__ = ["Attr", "Data", "Index", "Name"]


# standard library
from enum import Enum
from typing import Any, Collection, Hashable, Optional, TypeVar, Union


# dependencies
import numpy as np
from typing_extensions import (
    Annotated,
    Literal,
    get_args,
    get_origin,
    get_type_hints,
)


# type hints (private)
TAttr = TypeVar("TAttr", covariant=True)
TDtype = TypeVar("TDtype", covariant=True)
TName = TypeVar("TName", bound=Hashable, covariant=True)


# type hints (public)
class FieldType(Enum):
    """Annotations for pandas-related type hints."""

    ATTR = "attr"
    """Annotation for attribute fields."""

    DATA = "data"
    """Annotation for data fields."""

    INDEX = "index"
    """Annotation for index fields."""

    NAME = "name"
    """Annotation for name fields."""

    def annotates(self, type_: Any) -> bool:
        """Check if a type is annotated by the annotation."""
        return self in get_args(type_)[1:]


Attr = Annotated[TAttr, FieldType.ATTR]
"""Type hint for attribute fields (``Attr[TAttr]``)."""

Data = Annotated[Union[Collection[TDtype], TDtype], FieldType.DATA]
"""Type hint for data fields (``Data[TDtype]``)."""

Index = Annotated[Union[Collection[TDtype], TDtype], FieldType.INDEX]
"""Type hint for index fields (``Index[TDtype]``)."""

Name = Annotated[TName, FieldType.NAME]
"""Type hint for name fields (``Name[TName]``)."""


# runtime functions
def get_dtype(type_: Any) -> Optional[np.dtype[Any]]:
    """Parse a type and return a data type (dtype)."""
    try:
        t_dtype = get_args(unannotate(type_))[1]
    except (IndexError, NameError):
        raise ValueError(f"Could not convert {type_!r} to dtype.")

    if t_dtype is Any or t_dtype is type(None):
        return None

    if isinstance(t_dtype, type):
        return np.dtype(t_dtype)

    if get_origin(t_dtype) is Literal:
        return np.dtype(get_args(t_dtype)[0])

    raise ValueError(f"Could not convert {type_!r} to dtype.")


def get_ftype(type_: Any) -> FieldType:
    """Parse a type and return a field type (ftype)."""
    if FieldType.ATTR.annotates(type_):
        return FieldType.ATTR

    if FieldType.DATA.annotates(type_):
        return FieldType.DATA

    if FieldType.INDEX.annotates(type_):
        return FieldType.INDEX

    if FieldType.NAME.annotates(type_):
        return FieldType.NAME

    raise ValueError(f"Could not convert {type_!r} to ftype.")


def unannotate(type_: Any) -> Any:
    """Recursively remove annotations from a type."""

    class Temporary:
        __annotations__ = dict(type=type_)

    return get_type_hints(Temporary)["type"]
