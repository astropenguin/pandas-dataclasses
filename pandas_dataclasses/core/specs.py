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
from typing import Any, Callable, Hashable, List, Literal, Optional, Type


# dependencies
from typing_extensions import get_type_hints
from .typing import T, Pandas, Tag, get_dtype, get_name, get_tag


# runtime classes
@dataclass(frozen=True)
class Field:
    """Specification of a field."""

    id: str
    """Identifier of the field."""

    tag: Literal["attr", "column", "data", "index"]
    """Tag of the field."""

    name: Hashable = None
    """Name of the field data."""

    default: Any = None
    """Default value of the field data."""

    type: Optional[Any] = None
    """Type or type hint of the field data."""

    dtype: Optional[str] = None
    """Data type of the field data."""

    def update(self, obj: Any) -> "Field":
        """Update the specification by an object."""
        return replace(
            self,
            name=format_(self.name, obj),
            default=getattr(obj, self.id, self.default),
        )


class Fields(List[Field]):
    """List of field specifications (with selectors)."""

    @property
    def of_attr(self) -> "Fields":
        """Select only attribute field specifications."""
        return Fields(field for field in self if field.tag == "attr")

    @property
    def of_column(self) -> "Fields":
        """Select only column field specifications."""
        return Fields(field for field in self if field.tag == "column")

    @property
    def of_data(self) -> "Fields":
        """Select only data field specifications."""
        return Fields(field for field in self if field.tag == "data")

    @property
    def of_index(self) -> "Fields":
        """Select only index field specifications."""
        return Fields(field for field in self if field.tag == "index")

    def update(self, obj: Any) -> "Fields":
        """Update the specifications by an object."""
        return Fields(field.update(obj) for field in self)


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
        fields = Fields()

        for field_ in fields_(eval_types(dataclass)):
            if (field := get_field(field_)) is not None:
                fields.append(field)

        factory = getattr(dataclass, "__pandas_factory__", None)
        return cls(dataclass.__name__, dataclass, factory, fields)

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
def eval_types(dataclass: Type[T]) -> Type[T]:
    """Evaluate field types of a dataclass."""
    types = get_type_hints(dataclass, include_extras=True)

    for field_ in fields_(dataclass):
        field_.type = types[field_.name]

    return dataclass


def format_(obj: T, by: Any) -> T:
    """Format a string or nested strings in an object."""
    tp = type(obj)

    if isinstance(obj, str):
        return tp(obj.format(by))  # type: ignore
    elif isinstance(obj, (list, tuple, set)):
        return tp(format_(item, by) for item in obj)  # type: ignore
    elif isinstance(obj, dict):
        return tp(format_(item, by) for item in obj.items())  # type: ignore
    else:
        return obj


@lru_cache(maxsize=None)
def get_field(field_: "Field_[Any]") -> Optional[Field]:
    """Create a field specification from a dataclass field."""
    tag = get_tag(field_.type)

    if tag is Tag.OTHER:
        return None

    if tag in Tag.DATA | Tag.INDEX:
        dtype = get_dtype(field_.type)
    else:
        dtype = None

    return Field(
        id=field_.name,
        tag=tag.name.lower(),  # type: ignore
        name=get_name(field_.type, field_.name),
        default=field_.default,
        type=field_.type,
        dtype=dtype,
    )
