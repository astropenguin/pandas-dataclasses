__all__ = ["Attr", "Column", "Data", "Index", "Tag"]


# standard library
import types
from dataclasses import Field
from enum import Flag, auto
from itertools import chain
from typing import (
    Any,
    Callable,
    Collection,
    Dict,
    Hashable,
    Iterable,
    Literal,
    Optional,
    Protocol,
    Tuple,
    TypeVar,
    Union,
)


# dependencies
import pandas as pd
from pandas.api.types import pandas_dtype
from typing_extensions import Annotated, ParamSpec, get_args, get_origin


# type hints (private)
Pandas = Union[pd.DataFrame, "pd.Series[Any]"]
P = ParamSpec("P")
T = TypeVar("T")
TPandas = TypeVar("TPandas", bound=Pandas)
TFrame = TypeVar("TFrame", bound=pd.DataFrame)
TSeries = TypeVar("TSeries", bound="pd.Series[Any]")


class DataClass(Protocol[P]):
    """Type hint for dataclass objects."""

    __dataclass_fields__: Dict[str, "Field[Any]"]

    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        ...


class PandasClass(Protocol[P, TPandas]):
    """Type hint for dataclass objects with a pandas factory."""

    __dataclass_fields__: Dict[str, "Field[Any]"]
    __pandas_factory__: Callable[..., TPandas]

    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        ...


class Tag(Flag):
    """Collection of tags for annotating types."""

    ATTR = auto()
    """Tag for a type specifying an attribute field."""

    COLUMN = auto()
    """Tag for a type specifying a column field."""

    DATA = auto()
    """Tag for a type specifying a data field."""

    INDEX = auto()
    """Tag for a type specifying an index field."""

    DTYPE = auto()
    """Tag for a type specifying a data type."""

    FIELD = DATA | COLUMN | DATA | INDEX
    """Union of field-related tags."""

    ANY = FIELD | DTYPE
    """Union of all tags."""

    def annotates(self, tp: Any) -> bool:
        """Check if the tag annotates a type hint."""
        return any(map(self.includes, get_args(tp)))

    def excludes(self, obj: Any) -> bool:
        """Check if the tag excludes an object."""
        return not self.includes(obj)

    def includes(self, obj: Any) -> bool:
        """Check if the tag includes an object."""
        return isinstance(obj, type(self)) and obj in self

    def __repr__(self) -> str:
        """Return a hashtag-style string."""
        return str(self)

    def __str__(self) -> str:
        """Return a hashtag-style string."""
        return f"#{str(self.name).lower()}"


# type hints (public)
Attr = Annotated[T, Tag.ATTR]
"""Type hint for attribute fields (``Attr[T]``)."""

Column = Annotated[T, Tag.COLUMN]
"""Type hint for column fields (``Column[T]``)."""

Data = Annotated[Collection[T], Tag.DATA]
"""Type hint for data fields (``Data[T]``)."""

Index = Annotated[Collection[T], Tag.INDEX]
"""Type hint for index fields (``Index[T]``)."""


# runtime functions
def gen_annotated(tp: Any) -> Iterable[Any]:
    """Generate all annotated types in a type hint."""
    if get_origin(tp) is Annotated:
        yield tp
        yield from gen_annotated(get_args(tp)[0])
    else:
        yield from chain(*map(gen_annotated, get_args(tp)))


def get_tagged(
    tp: Any,
    bound: Tag = Tag.ANY,
    keep_annotations: bool = False,
) -> Optional[Any]:
    """Extract the first tagged type from a type hint."""
    for tagged in filter(bound.annotates, gen_annotated(tp)):
        return tagged if keep_annotations else get_args(tagged)[0]


def get_tags(tp: Any, bound: Tag = Tag.ANY) -> Optional[Tuple[Tag, ...]]:
    """Extract all tags from the first tagged type in a type hint."""
    if (tagged := get_tagged(tp, bound, True)) is not None:
        return tuple(filter(bound.includes, get_args(tagged)[1:]))


def get_nontags(tp: Any, bound: Tag = Tag.ANY) -> Optional[Tuple[Any, ...]]:
    """Extract all except tags from the first tagged type in a type hint."""
    if (tagged := get_tagged(tp, bound, True)) is not None:
        return tuple(filter(bound.excludes, get_args(tagged)[1:]))


def get_dtype(tp: Any) -> Optional[str]:
    """Extract a data type of NumPy or pandas from a type hint."""
    if (tagged := get_tagged(tp, Tag.DATA | Tag.INDEX)) is None:
        return None

    if (dtype := get_tagged(tagged, Tag.DTYPE)) is None:
        return None

    if dtype is Any or dtype is type(None):
        return None

    if is_union_type(dtype):
        dtype = get_args(dtype)[0]

    if get_origin(dtype) is Literal:
        dtype = get_args(dtype)[0]

    return pandas_dtype(dtype).name


def get_name(tp: Any, default: Hashable = None) -> Hashable:
    """Extract a name if found or return given default."""
    try:
        name = get_annotations(tp)[1]
    except (IndexError, TypeError):
        return default

    if name is Ellipsis:
        return default

    try:
        hash(name)
    except TypeError:
        raise ValueError("Could not find any valid name.")

    return name  # type: ignore


def get_tag(tp: Any, default: Tag = Tag.OTHER) -> Tag:
    """Extract a tag if found or return given default."""
    try:
        return get_annotations(tp)[0]  # type: ignore
    except (IndexError, TypeError):
        return default


def is_union_type(tp: Any) -> bool:
    """Check if a type hint is a union type."""
    if get_origin(tp) is Union:
        return True

    UnionType = getattr(types, "UnionType", None)
    return UnionType is not None and isinstance(tp, UnionType)
