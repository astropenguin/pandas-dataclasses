__all__ = ["Spec"]


# standard library
from dataclasses import dataclass, replace
from dataclasses import Field as Field_, fields as fields_
from functools import lru_cache
from typing import Any, Hashable, List, Optional, Type


# dependencies
from typing_extensions import Literal, get_type_hints


# submodules
from .typing import (
    P,
    AnyDType,
    AnyName,
    AnyPandas,
    DataClass,
    Role,
    get_dtype,
    get_name,
    get_role,
)


# runtime classes
@dataclass(frozen=True)
class Field:
    """Specification of a field."""

    id: str
    """Identifier of the field."""

    name: AnyName
    """Name of the field."""

    role: Literal["attr", "data", "index"]
    """Role of the field."""

    type: Optional[Any]
    """Type (hint) of the field data."""

    dtype: Optional[AnyDType]
    """Data type of the field data."""

    default: Any
    """Default value of the field data."""

    @property
    def hashable_name(self) -> Hashable:
        """Hashable name of the field."""
        if isinstance(self.name, dict):
            return tuple(self.name.values())
        else:
            return self.name

    def update(self, obj: DataClass[P]) -> "Field":
        """Update the specification by a dataclass object."""
        return replace(
            self,
            name=format_name(self.name, obj),
            default=getattr(obj, self.id),
        )


class Fields(List[Field]):
    """List of field specifications (with selectors)."""

    @property
    def of_attr(self) -> "Fields":
        """Select only attribute field specifications."""
        return Fields(field for field in self if field.role == "attr")

    @property
    def of_data(self) -> "Fields":
        """Select only data field specifications."""
        return Fields(field for field in self if field.role == "data")

    @property
    def of_index(self) -> "Fields":
        """Select only index field specifications."""
        return Fields(field for field in self if field.role == "index")

    def update(self, obj: DataClass[P]) -> "Fields":
        """Update the specifications by a dataclass object."""
        return Fields(field.update(obj) for field in self)


@dataclass(frozen=True)
class Spec:
    """Specification of a pandas dataclass."""

    fields: Fields
    """List of field specifications."""

    factory: Optional[Type[AnyPandas]] = None
    """Factory for pandas data creation."""

    @classmethod
    def from_dataclass(cls, dataclass: Type[DataClass[P]]) -> "Spec":
        """Create a specification from a data class."""
        fields = Fields()

        for field_ in fields_(eval_types(dataclass)):
            field = convert_field(field_)

            if field is not None:
                fields.append(field)

        factory = getattr(dataclass, "__pandas_factory__", None)
        return cls(fields, factory)

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
    role = get_role(field_.type)

    if role is Role.ATTR:
        role = "attr"
    elif role is Role.DATA:
        role = "data"
    elif role is Role.INDEX:
        role = "index"
    else:
        return

    return Field(
        id=field_.name,
        name=get_name(field_.type, field_.name),
        role=role,
        type=field_.type,
        dtype=get_dtype(field_.type),
        default=field_.default,
    )


@lru_cache(maxsize=None)
def eval_types(dataclass: Type[DataClass[P]]) -> Type[DataClass[P]]:
    """Evaluate field types of a dataclass."""
    types = get_type_hints(dataclass, include_extras=True)

    for field in fields_(dataclass):
        field.type = types[field.name]

    return dataclass


def format_name(name: AnyName, obj: DataClass[P]) -> AnyName:
    """Format a name by a dataclass object."""
    if isinstance(name, str):
        return name.format(obj)

    if isinstance(name, dict):
        formatted: "dict[Hashable, Hashable]" = {}

        for key, val in name.items():
            key = key.format(obj) if isinstance(key, str) else key
            val = val.format(obj) if isinstance(val, str) else val
            formatted[key] = val

        return formatted

    return name
