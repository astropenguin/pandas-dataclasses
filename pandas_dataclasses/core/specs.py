__all__ = ["Spec"]


# standard library
from dataclasses import (
    Field as Field_,
    dataclass,
    field as field_,
    fields as fields_,
    replace,
)
from functools import lru_cache
from itertools import repeat
from typing import (
    Any,
    Callable,
    Collection,
    Hashable,
    List,
    Literal,
    Mapping,
    Optional,
    Tuple,
    cast,
)


# dependencies
from pandas.api.types import pandas_dtype
from typing_extensions import get_args, get_origin, get_type_hints
from .tagging import Tag, get_nontags, get_tagged, get_tags
from .typing import TAny, Pandas, is_union


@dataclass(frozen=True)
class Field:
    """Specification of a field."""

    id: str
    """Identifier of the field."""

    name: Hashable
    """Name of the field data."""

    tags: Tuple[Tag, ...] = ()
    """Tags of the field."""

    type: Optional[Any] = None
    """Type or type hint of the field data."""

    dtype: Optional[str] = None
    """Data type of the field data."""

    default: Any = None
    """Default value of the field data."""

    def has(self, tag: Tag) -> bool:
        """Check if the specification has a tag."""
        return bool(tag & Tag.union(self.tags))

    def update(self, obj: Any) -> "Field":
        """Update the specification by an object."""
        return replace(
            self,
            name=format_(self.name, obj),
            default=getattr(obj, self.id, self.default),
        )


class Fields(List[Field]):
    """List of field specifications with selectors."""

    def of(self, tag: Tag) -> "Fields":
        """Select only fields that have a tag."""
        return type(self)(filter(lambda field: field.has(tag), self))

    def update(self, obj: Any) -> "Fields":
        """Update the specifications by an object."""
        return type(self)(field.update(obj) for field in self)


@dataclass(frozen=True)
class Spec:
    """Specification of pandas data creation."""

    name: Optional[str] = None
    """Name of the specification."""

    origin: Optional[type] = None
    """Original dataclass of the specification."""

    factory: Optional[Callable[..., Pandas]] = None
    """Factory for pandas data creation."""

    fields: Fields = field_(default_factory=Fields)
    """List of field specifications."""

    @classmethod
    def from_dataclass(cls, dataclass: type) -> "Spec":
        """Create a specification from a data class."""
        eval_field_types(dataclass)

        return cls(
            name=dataclass.__name__,
            origin=dataclass,
            factory=getattr(dataclass, "__pandas_factory__", None),
            fields=Fields(map(convert_field, fields_(dataclass))),
        )

    def update(self, obj: Any) -> "Spec":
        """Update the specification by an object."""
        if self.origin is None or isinstance(obj, self.origin):
            return replace(self, fields=self.fields.update(obj))
        else:
            return self.update(self.origin(obj))

    def __matmul__(self, obj: Any) -> "Spec":
        """Alias of the update method."""
        return self.update(obj)


@lru_cache(maxsize=None)
def convert_field(field_: "Field_[Any]") -> Field:
    """Convert a dataclass field to a field specification."""
    return Field(
        id=field_.name,
        name=get_name(field_.type, field_.name),
        tags=get_tags(field_.type, Tag.FIELD),
        type=field_.type,
        dtype=get_dtype(field_.type),
        default=field_.default,
    )


@lru_cache(maxsize=None)
def eval_field_types(dataclass: type) -> None:
    """Evaluate field types of a dataclass."""
    types = get_type_hints(dataclass, include_extras=True)

    for field_ in fields_(dataclass):
        field_.type = types[field_.name]


def format_(obj: TAny, by: Any) -> TAny:
    """Format a string or nested strings in an object."""
    tp = type(obj)

    if isinstance(obj, str):
        return tp(obj.format(by))  # type: ignore

    if isinstance(obj, Mapping):
        return tp(map(format_, obj.items(), repeat(by)))  # type: ignore

    if isinstance(obj, Collection):
        return tp(map(format_, obj, repeat(by)))  # type: ignore

    return obj


def get_dtype(tp: Any) -> Optional[str]:
    """Extract a data type of NumPy or pandas from a type hint."""
    if (tp := get_tagged(tp, Tag.DATA | Tag.INDEX, True)) is None:
        return None

    if (dtype := get_tagged(tp, Tag.DTYPE)) is None:
        return None

    if dtype is Any or dtype is type(None):
        return None

    if is_union(dtype):
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
