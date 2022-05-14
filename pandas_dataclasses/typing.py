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
    Iterable,
    Optional,
    Tuple,
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

        return any(isinstance(arg, cls) for arg in get_args(tp))


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
    """Recursively remove annotations in a type hint."""

    class Temporary:
        __annotations__ = dict(type=tp)

    return get_type_hints(Temporary)["type"]


def find_annotated(tp: Any) -> Iterable[Any]:
    """Generate all annotated types in a type hint."""
    args = get_args(tp)

    if get_origin(tp) is Annotated:
        yield tp
        yield from find_annotated(args[0])
    else:
        yield from chain(*map(find_annotated, args))


def get_annotated(tp: Any) -> Any:
    """Extract the first ftype-annotated type."""
    for annotated in filter(FType.annotates, find_annotated(tp)):
        return deannotate(annotated)

    raise TypeError("Could not find any ftype-annotated type.")


def get_annotations(tp: Any) -> Tuple[Any, ...]:
    """Extract annotations of the first ftype-annotated type."""
    for annotated in filter(FType.annotates, find_annotated(tp)):
        return get_args(annotated)[1:]

    raise TypeError("Could not find any ftype-annotated type.")


def get_dtype(tp: Any) -> Optional[AnyDType]:
    """Extract a NumPy or pandas data type."""
    try:
        dtype = get_args(get_annotated(tp))[1]
    except TypeError:
        raise TypeError(f"Could not find any dtype in {tp!r}.")

    if dtype is Any or dtype is type(None):
        return

    if get_origin(dtype) is Literal:
        dtype = get_args(dtype)[0]

    return pandas_dtype(dtype)  # type: ignore


def get_ftype(tp: Any, default: FType = FType.OTHER) -> FType:
    """Extract an ftype if found or return given default."""
    try:
        return get_annotations(tp)[0]
    except TypeError:
        return default


def get_name(tp: Any, default: Hashable = None) -> Hashable:
    """Extract a name if found or return given default."""
    try:
        annotations = get_annotations(tp)[1:]
    except TypeError:
        return default

    for annotation in annotations:
        if isinstance(annotation, Hashable):
            return annotation

    return default
