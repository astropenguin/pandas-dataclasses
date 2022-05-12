__all__ = ["Attr", "Data", "Index", "Name", "Other"]


# standard library
from dataclasses import Field
from enum import Enum
from itertools import chain
from typing import (
    Any,
    ClassVar,
    Collection,
    Dict,
    Hashable,
    Iterator,
    Optional,
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

    @classmethod
    def annotates(cls, tp: Any) -> bool:
        """Check if any ftype annotates a type hint."""
        if get_origin(tp) is not Annotated:
            return False

        for annotation in get_args(tp)[1:]:
            if isinstance(annotation, cls):
                return True

        return False


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


def get_annotated(tp: Any) -> Iterator[Any]:
    """Extract all annotated types from a type hint."""
    args = get_args(tp)

    if get_origin(tp) is Annotated:
        yield tp
        yield from get_annotated(args[0])
    else:
        yield from chain(*map(get_annotated, args))


def get_dtype(tp: Any) -> Optional[AnyDType]:
    """Extract a dtype (most outer data type) from a type hint."""
    tps = list(filter(FType.annotates, get_annotated(tp)))

    if len(tps) == 0:
        raise TypeError(f"Could not find any dtype in {tp!r}.")

    dtype = get_args(get_args(tps[-1])[0])[1]

    if dtype is Any or dtype is type(None):
        return

    if get_origin(dtype) is Literal:
        dtype = get_args(dtype)[0]

    return pandas_dtype(dtype)  # type: ignore


def get_ftype(tp: Any, default: FType = FType.OTHER) -> FType:
    """Extract an ftype (most outer FType) from a type hint."""
    tps = list(filter(FType.annotates, get_annotated(tp)))

    if len(tps) == 0:
        return default

    annotations = get_args(tps[-1])[1:]

    for annotation in reversed(annotations):
        if isinstance(annotation, FType):
            return annotation

    return default


def get_name(tp: Any, default: Hashable = None) -> Hashable:
    """Extract a name (most outer hashable) from a type hint."""
    tps = list(filter(FType.annotates, get_annotated(tp)))

    if len(tps) == 0:
        return default

    annotations = get_args(tps[-1])[1:]

    for annotation in reversed(annotations):
        if isinstance(annotation, FType):
            continue

        if isinstance(annotation, Hashable):
            return annotation

    return default
