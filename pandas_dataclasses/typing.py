__all__ = ["Attr", "Data", "Index", "Name", "Other"]


# standard library
from dataclasses import Field
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Collection,
    Dict,
    Hashable,
    Optional,
    Type,
    TypeVar,
    Union,
)


# dependencies
from numpy import dtype
from pandas.api.extensions import ExtensionDtype
from pandas.api.types import pandas_dtype  # type: ignore
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
AnyDType: TypeAlias = Union["dtype[Any]", ExtensionDtype]
AnyField: TypeAlias = "Field[Any]"
T = TypeVar("T")
TCovariant = TypeVar("TCovariant", covariant=True)
THashable = TypeVar("THashable", bound=Hashable)


class Collection(Collection[TCovariant], Protocol):
    """Type hint equivalent to typing.Collection."""

    pass


class DataClass(Protocol):
    """Type hint for dataclass objects."""

    __dataclass_fields__: ClassVar[Dict[str, AnyField]]


class FType(Enum):
    """Annotations for typing dataclass fields."""

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
    """Recursively remove annotations from a type hint."""

    class Temporary:
        __annotations__ = dict(type=tp)

    return get_type_hints(Temporary)["type"]


def get_collection(tp: Any) -> Type[Collection[Any]]:
    """Extract the first collection type from a type hint."""
    tp = deannotate(tp)

    if get_origin(tp) is not Union:
        raise TypeError(f"{tp!r} was not a union type.")

    for arg in get_args(tp):
        if get_origin(arg) is Collection:
            return arg

    raise TypeError(f"{tp!r} had no collection type.")


def get_dtype(tp: Any) -> Optional[AnyDType]:
    """Extract a dtype (the first data type) from a type hint."""
    dtype = get_args(get_collection(tp))[0]

    if dtype is Any or dtype is type(None):
        return

    if get_origin(dtype) is Literal:
        dtype = get_args(dtype)[0]

    return pandas_dtype(dtype)  # type: ignore


def get_ftype(tp: Any, default: FType = FType.OTHER) -> FType:
    """Extract an ftype (most outer FType) from a type hint."""
    if get_origin(tp) is not Annotated:
        return default

    for ann in reversed(get_args(tp)[1:]):
        if isinstance(ann, FType):
            return ann

    return default


def get_name(tp: Any, default: Hashable = None) -> Hashable:
    """Extract a name (most outer hashable) from a type hint."""
    if get_origin(tp) is not Annotated:
        return default

    for ann in reversed(get_args(tp)[1:]):
        if isinstance(ann, FType):
            continue

        if isinstance(ann, Hashable):
            return ann

    return default
