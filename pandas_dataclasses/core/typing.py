__all__ = ["Attr", "Column", "Data", "Index", "Tag"]


# standard library
import types
from dataclasses import Field
from enum import Flag, auto
from functools import reduce
from itertools import chain, filterfalse
from operator import or_
from typing import (
    Any,
    Callable,
    Collection,
    Dict,
    Hashable,
    Iterable,
    List,
    Literal,
    Optional,
    Protocol,
    TypeVar,
    Union,
    cast,
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

    FIELD = ATTR | COLUMN | DATA | INDEX
    """Union of field-related tags."""

    ANY = FIELD | DTYPE
    """Union of all tags."""

    def annotates(self, tp: Any) -> bool:
        """Check if the tag annotates a type hint."""
        return any(map(self.covers, get_args(tp)))

    def covers(self, obj: Any) -> bool:
        """Check if the tag is superset of an object."""
        return type(self).creates(obj) and obj in self

    @classmethod
    def creates(cls, obj: Any) -> bool:
        """Check if Tag is the type of an object."""
        return isinstance(obj, cls)

    @classmethod
    def union(cls, tags: Iterable["Tag"]) -> "Tag":
        """Create a tag as an union of tags."""
        return reduce(or_, tags, Tag(0))

    def __repr__(self) -> str:
        """Return the hashtag-style string of the tag."""
        return str(self)

    def __str__(self) -> str:
        """Return the hashtag-style string of the tag."""
        return f"#{str(self.name).lower()}"


# type hints (public)
Attr = Annotated[T, Tag.ATTR]
"""Type hint for attribute fields (``Attr[T]``)."""

Column = Annotated[T, Tag.COLUMN]
"""Type hint for column fields (``Column[T]``)."""

Data = Annotated[Collection[Annotated[T, Tag.DTYPE]], Tag.DATA]
"""Type hint for data fields (``Data[T]``)."""

Index = Annotated[Collection[Annotated[T, Tag.DTYPE]], Tag.INDEX]
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


def get_tags(tp: Any, bound: Tag = Tag.ANY) -> List[Tag]:
    """Extract all tags from the first tagged type."""
    tagged = get_tagged(tp, bound, True)
    return list(filter(Tag.creates, get_args(tagged)[1:]))


def get_nontags(tp: Any, bound: Tag = Tag.ANY) -> List[Any]:
    """Extract all except tags from the first tagged type."""
    tagged = get_tagged(tp, bound, True)
    return list(filterfalse(Tag.creates, get_args(tagged)[1:]))


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
    """Extract the first hashable as a name from a type hint."""
    if not (nontags := get_nontags(tp, Tag.FIELD)):
        return default

    if (name := nontags[0]) is Ellipsis:
        return default

    hash(name)
    return cast(Hashable, name)


def is_union_type(tp: Any) -> bool:
    """Check if a type hint is a union type."""
    if get_origin(tp) is Union:
        return True

    UnionType = getattr(types, "UnionType", None)
    return UnionType is not None and isinstance(tp, UnionType)
