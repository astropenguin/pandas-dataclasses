__all__ = ["DataSpec"]


# standard library
from dataclasses import Field, dataclass, field, fields
from typing import Any, Dict, Hashable, Optional, Type, Union


# dependencies
import numpy as np
from typing_extensions import Literal, ParamSpec, get_type_hints


# submodules
from .typing import DataClass, FieldType, deannotate, get_dtype, get_ftype, get_name


# type hints
FieldSpec = Union["ArrayFieldSpec", "MetaFieldSpec"]
PInit = ParamSpec("PInit")


# runtime classes
class MissingType:
    """Singleton that indicates missing data."""

    def __repr__(self) -> str:
        return "<MISSING>"


MISSING = MissingType()


@dataclass(frozen=True)
class ArraySpec:
    """Specification for arrays."""

    type: Optional["np.dtype[Any]"]
    """Data type of the array."""

    default: Any
    """Default value of the array."""

    def __call__(self, obj: Any = MISSING) -> "np.ndarray[Any, Any]":
        """Convert an object be spec-compliant."""
        if obj is MISSING:
            obj = self.default

        return np.asarray(obj, dtype=self.type)


@dataclass(frozen=True)
class MetaSpec:
    """Specification for metadata."""

    type: Any
    """Type of the metadata."""

    default: Any
    """Default value of the metadata."""

    def __call__(self, obj: Any = MISSING) -> Any:
        """Convert an object be spec-compliant."""
        if obj is MISSING:
            obj = self.default

        return obj


@dataclass(frozen=True)
class ArrayFieldSpec:
    """Specification for array fields."""

    type: Literal["data", "index"]
    """Type of the field."""

    name: Hashable
    """Name of the field."""

    data: ArraySpec
    """Data specification of the field."""


@dataclass(frozen=True)
class MetaFieldSpec:
    """Specification for metadata fields."""

    type: Literal["attr", "name"]
    """Type of the field."""

    name: Hashable
    """Name of the field."""

    data: MetaSpec
    """Data specification of the field."""


@dataclass(frozen=True)
class DataSpec:
    """Specification for pandas dataclasses."""

    fields: Dict[str, FieldSpec] = field(default_factory=dict)
    """Field specifications of the dataclass."""

    @classmethod
    def from_dataclass(
        cls,
        dataclass: Type[DataClass[PInit]],
        cache: bool = True,
    ) -> "DataSpec":
        """Create a specification from a dataclass."""
        if cache and hasattr(dataclass, "__dataspec__"):
            return dataclass.__dataspec__  # type: ignore

        dataspec = cls()
        eval_fields(dataclass)

        for field in fields(dataclass):
            fieldspec = get_fieldspec(field)

            if fieldspec is not None:
                dataspec.fields[field.name] = fieldspec

        dataclass.__dataspec__ = dataspec  # type: ignore
        return dataspec


# runtime functions
def eval_fields(dataclass: Type[DataClass[PInit]]) -> None:
    """Evaluate types of dataclass fields."""
    types = get_type_hints(dataclass, include_extras=True)

    for field in fields(dataclass):
        field.type = types[field.name]


def get_fieldspec(field: "Field[Any]") -> Optional[FieldSpec]:
    """Parse a dataclass field and return a field specification."""
    ftype = get_ftype(field.type)
    name = get_name(field.type, field.name)

    if ftype is FieldType.DATA or ftype is FieldType.INDEX:
        return ArrayFieldSpec(
            type=ftype.value,
            name=name,
            data=ArraySpec(get_dtype(field.type), field.default),
        )

    if ftype is FieldType.ATTR or ftype is FieldType.NAME:
        return MetaFieldSpec(
            type=ftype.value,
            name=name,
            data=MetaSpec(deannotate(field.type), field.default),
        )
