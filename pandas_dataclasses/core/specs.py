__all__ = ["Spec"]


# standard library
from dataclasses import (
    MISSING,
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
from .typing import P, DataClass, Pandas, Tag, get_dtype, get_name, get_tag


# runtime classes
@dataclass(frozen=True)
class Field:
    """Specification of a field."""

    id: str
    """Identifier of the field."""

    name: Hashable
    """Name of the field."""

    tag: Literal["attr", "column", "data", "index"]
    """Tag of the field."""

    default: Any = MISSING
    """Default value of the field data."""

    type: Optional[Any] = None
    """Type (hint) of the field data."""

    dtype: Optional[str] = None
    """Data type of the field data."""

    def update(self, obj: DataClass[P]) -> "Field":
        """Update the specification by a dataclass object."""
        return replace(
            self,
            name=format_name(self.name, obj),
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

    def update(self, obj: DataClass[P]) -> "Fields":
        """Update the specifications by a dataclass object."""
        return Fields(field.update(obj) for field in self)


@dataclass(frozen=True)
class Spec:
    """Specification of pandas data creation."""

    name: Optional[str] = None
    """Name of the specification."""

    factory: Optional[Callable[..., Pandas]] = None
    """Factory for pandas data creation."""

    fields: Fields = field_(default_factory=Fields)
    """List of field specifications."""

    @classmethod
    def from_dataclass(cls, dataclass: Type[DataClass[P]]) -> "Spec":
        """Create a specification from a data class."""
        fields = Fields()

        for field_ in fields_(eval_types(dataclass)):
            field = convert_field(field_)

            if field is not None:
                fields.append(field)

        factory = getattr(dataclass, "__pandas_factory__", None)
        return cls(dataclass.__name__, factory, fields)

    def update(self, obj: DataClass[P]) -> "Spec":
        """Update the specification by a dataclass object."""
        return replace(self, fields=self.fields.update(obj))

    def __matmul__(self, obj: DataClass[P]) -> "Spec":
        """Alias of the update method."""
        return self.update(obj)


# runtime functions
@lru_cache(maxsize=None)
def convert_field(field_: "Field_[Any]") -> Optional[Field]:
    """Convert a dataclass field to a field specification."""
    tag = get_tag(field_.type)

    if tag is Tag.OTHER:
        return None

    return Field(
        id=field_.name,
        name=get_name(field_.type, field_.name),
        tag=tag.name.lower(),  # type: ignore
        default=field_.default,
        type=field_.type,
        dtype=get_dtype(field_.type),
    )


@lru_cache(maxsize=None)
def eval_types(dataclass: Type[DataClass[P]]) -> Type[DataClass[P]]:
    """Evaluate field types of a dataclass."""
    types = get_type_hints(dataclass, include_extras=True)

    for field_ in fields_(dataclass):
        field_.type = types[field_.name]

    return dataclass


def format_name(name: Hashable, obj: DataClass[P]) -> Hashable:
    """Format a name by a dataclass object."""
    if isinstance(name, tuple):
        return type(name)(format_name(elem, obj) for elem in name)

    if isinstance(name, str):
        return name.format(obj)

    return name
