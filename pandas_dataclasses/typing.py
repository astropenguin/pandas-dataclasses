__all__ = ["Attr", "Data", "Index", "Name", "Other"]


# standard library
from dataclasses import Field
from enum import Enum
from typing import Any, ClassVar, Collection, Dict, Hashable, Optional, TypeVar, Union


# dependencies
import numpy as np
from typing_extensions import (
    Annotated,
    Literal,
    Protocol,
    TypeAlias,
    get_args,
    get_origin,
    get_type_hints,
)


# type variables (private)
T = TypeVar("T")
THashable = TypeVar("THashable", bound=Hashable)


# type hints (private)
AnyDType: TypeAlias = "np.dtype[Any]"
AnyField: TypeAlias = "Field[Any]"


class DataClass(Protocol):
    """Type hint for dataclass objects."""

    __dataclass_fields__: ClassVar[Dict[str, AnyField]]


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


# type hints (public)
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
def deannotate(tp: Any) -> Any:
    """Recursively remove annotations from a type."""

    class Temporary:
        __annotations__ = dict(type=tp)

    return get_type_hints(Temporary)["type"]


def get_dtype(tp: Any) -> Optional[AnyDType]:
    """Parse a type and return a data type (dtype)."""
    tp = deannotate(tp)

    if get_origin(tp) is not Union:
        raise TypeError(f"{tp!r} is not arrayable.")

    try:
        vector, scalar = get_args(tp)
    except ValueError:
        raise TypeError(f"{tp!r} is not arrayable.")

    if get_args(vector)[0] is not scalar:
        raise TypeError(f"{tp!r} is not arrayable.")

    if scalar is Any or scalar is type(None):
        return None

    if get_origin(scalar) is Literal:
        scalar = get_args(scalar)[0]

    return np.dtype(scalar)


def get_ftype(tp: Any, default: FType = FType.OTHER) -> FType:
    """Parse a type and return a field type (ftype)."""
    if get_origin(tp) is not Annotated:
        return default

    for arg in reversed(get_args(tp)[1:]):
        if isinstance(arg, FType):
            return arg

    return default


def get_name(tp: Any, default: Hashable = None) -> Hashable:
    """Parse a type and return a name."""
    if get_origin(tp) is not Annotated:
        return default

    for arg in reversed(get_args(tp)[1:]):
        if isinstance(arg, FType):
            continue

        if isinstance(arg, Hashable):
            return arg

    return default
