__all__ = ["Data", "Index", "NamedData", "NamedIndex"]


# standard library
from enum import Enum
from typing import Any, Collection, Hashable, Optional, TypeVar, Union


# dependencies
from typing_extensions import (
    Annotated,
    Literal,
    Protocol,
    get_args,
    get_origin,
    get_type_hints,
)


# type hints (private)
TDtype = TypeVar("TDtype", covariant=True)
TName = TypeVar("TName", bound=Hashable, covariant=True)


class Named(Protocol[TName]):
    """Type hint for named objects."""

    pass


class Collection(Named[TName], Collection[TDtype], Protocol):
    """Type hint for named collection objects."""

    pass


# type hints (public)
class FieldType(Enum):
    """Annotations for pandas-related type hints."""

    DATA = "data"
    """Annotation for data fields."""

    INDEX = "index"
    """Annotation for index fields."""

    def annotates(self, type_: Any) -> bool:
        """Check if a type is annotated by the annotation."""
        return self in get_args(type_)[1:]


Data = Annotated[Union[Collection[None, TDtype], TDtype], FieldType.DATA]
"""Type hint for data fields (``Data[TDtype]``)."""

Index = Annotated[Union[Collection[None, TDtype], TDtype], FieldType.INDEX]
"""Type hint for index fields (``Index[TDtype]``)."""

NamedData = Annotated[Union[Collection[TName, TDtype], TDtype], FieldType.DATA]
"""Type hint for named data fields (``NamedData[TName, TDtype]``)."""

NamedIndex = Annotated[Union[Collection[TName, TDtype], TDtype], FieldType.INDEX]
"""Type hint for named index fields (``NamedIndex[TName, TDtype]``)."""


# runtime functions
def get_dtype(type_: Any) -> Optional[str]:
    """Parse a type and return a dtype."""
    args = get_args(type_)
    origin = get_origin(type_)

    if origin is Collection:
        return get_dtype(args[1])

    if origin is Literal:
        return args[0]

    if type_ is Any or type_ is type(None):
        return None

    if isinstance(type_, type):
        return type_.__name__

    raise ValueError(f"Could not convert {type_!r} to dtype.")


def get_ftype(type_: Any) -> FieldType:
    """Parse a type and return a field type (ftype)."""
    if FieldType.DATA.annotates(type_):
        return FieldType.DATA

    if FieldType.INDEX.annotates(type_):
        return FieldType.INDEX

    raise ValueError(f"Could not convert {type_!r} to ftype.")


def get_name(type_: Any) -> Optional[Hashable]:
    """Parse a type and return a name."""
    args = get_args(type_)
    origin = get_origin(type_)

    if origin is Collection:
        return get_dtype(args[0])

    if origin is Literal:
        return args[0]

    if type_ is type(None):
        return None

    raise ValueError(f"Could not convert {type_!r} to name.")


def get_rtype(type_: Any) -> Any:
    """Parse a type and return a representative type (rtype)."""

    class Temporary:
        __annotations__ = dict(type=type_)

    try:
        unannotated = get_type_hints(Temporary)["type"]
    except NameError:
        raise ValueError(f"Could not convert {type_!r} to rtype.")

    if get_origin(unannotated) is Union:
        return get_args(unannotated)[0]
    else:
        return unannotated
