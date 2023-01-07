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
from typing import Any, Callable, Collection, Hashable, List, Mapping, Optional


# dependencies
from typing_extensions import get_type_hints
from .typing import T, Pandas, Tag, get_dtype, get_name, get_tags


# runtime classes
@dataclass(frozen=True)
class Field:
    """Specification of a field."""

    id: str
    """Identifier of the field."""

    name: Hashable
    """Name of the field data."""

    tags: List[Tag] = field_(default_factory=list)
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


# runtime functions
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


def format_(obj: T, by: Any) -> T:
    """Format a string or nested strings in an object."""
    tp = type(obj)

    if isinstance(obj, str):
        return tp(obj.format(by))  # type: ignore

    if isinstance(obj, Mapping):
        return tp(map(format_, obj.items(), repeat(by)))  # type: ignore

    if isinstance(obj, Collection):
        return tp(map(format_, obj, repeat(by)))  # type: ignore

    return obj
