__all__ = ["Attr", "Data", "Index", "Name", "Other"]


# standard library
from dataclasses import Field
from enum import Enum
from typing import Any, ClassVar, Collection, Dict, Hashable, Optional, TypeVar, Union


# dependencies
from numpy import dtype, ndarray
from typing_extensions import (
    Annotated,
    Literal,
    Protocol,
    TypeAlias,
    get_args,
    get_origin,
    get_type_hints,
)


# type hints (private)
AnyArray: TypeAlias = "ndarray[Any, Any]"
AnyDType: TypeAlias = "dtype[Any]"
AnyField: TypeAlias = "Field[Any]"
T = TypeVar("T")
THashable = TypeVar("THashable", bound=Hashable)


class DataClass(Protocol):
    """Type hint for dataclass objects."""

    __dataclass_fields__: ClassVar[Dict[str, AnyField]]


# type hints (public)
class FType(Enum):
    """Annotations for pandas-related type hints."""

    ATTR = "attr"
    """Annotation for attribute fields."""

    DATA = "data"
    """Annotation for data fields."""

    INDEX = "index"
    """Annotation for index fields."""

    NAME = "name"
    """Annotation for name fields."""

    OTHER = "other"
    """Annotation for other fields."""


Attr = Annotated[T, FType.ATTR]
"""Type hint for attribute fields (``Attr[T]``)."""

Data = Annotated[Union[Collection[T], T], FType.DATA]
"""Type hint for data fields (``Data[T]``)."""

Index = Annotated[Union[Collection[T], T], FType.INDEX]
"""Type hint for index fields (``Index[T]``)."""

Name = Annotated[THashable, FType.NAME]
"""Type hint for name fields (``Name[T]``)."""

Other = Annotated[T, FType.OTHER]
"""Type hint for other fields (``Other[T]``)."""


# runtime functions
def deannotate(type_: Any) -> Any:
    """Recursively remove annotations from a type."""

    class Temporary:
        __annotations__ = dict(type=type_)

    return get_type_hints(Temporary)["type"]


def get_dtype(type_: Any) -> Optional[AnyDType]:
    """Parse a type and return a data type (dtype)."""
    try:
        t_dtype = get_args(deannotate(type_))[1]
    except (IndexError, NameError):
        raise ValueError(f"Could not convert {type_!r} to dtype.")

    if t_dtype is Any or t_dtype is type(None):
        return None

    if get_origin(t_dtype) is Literal:
        return dtype(get_args(t_dtype)[0])

    if isinstance(t_dtype, type):
        return dtype(t_dtype)

    raise ValueError(f"Could not convert {type_!r} to dtype.")


def get_ftype(type_: Any, default: FType = FType.OTHER) -> FType:
    """Parse a type and return a field type (ftype)."""
    if get_origin(type_) is not Annotated:
        return default

    for arg in reversed(get_args(type_)[1:]):
        if isinstance(arg, FType):
            return arg

    return default


def get_name(type_: Any, default: Hashable = None) -> Hashable:
    """Parse a type and return a name."""
    if get_origin(type_) is not Annotated:
        return default

    for arg in reversed(get_args(type_)[1:]):
        if isinstance(arg, FType):
            continue

        if isinstance(arg, Hashable):
            return arg

    return default
