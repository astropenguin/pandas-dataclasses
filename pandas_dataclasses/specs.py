__all__ = ["DataSpec"]


# standard library
from dataclasses import dataclass, field, fields
from functools import lru_cache
from typing import Any, Dict, Hashable, Optional, Type, TypeVar, Union


# dependencies
from typing_extensions import Literal, get_type_hints


# submodules
from .typing import (
    AnyDType,
    AnyField,
    DataClass,
    FType,
    get_annotated,
    get_dtype,
    get_ftype,
    get_name,
)


# type hints
AnyFieldSpec = Union["ArrayFieldSpec", "ScalarFieldSpec"]
TDataClass = TypeVar("TDataClass", bound=DataClass)


# runtime classes
@dataclass(frozen=True)
class ArraySpec:
    """Specification of arrays."""

    type: Optional[AnyDType]
    """Data type of the array."""

    default: Any
    """Default value of the array."""


@dataclass(frozen=True)
class ScalarSpec:
    """Specification of scalars."""

    type: Any
    """Type of the scalar."""

    default: Any
    """Default value of the scalar."""


@dataclass(frozen=True)
class ArrayFieldSpec:
    """Specification of array fields."""

    type: Literal["data", "index"]
    """Type of the field."""

    name: Hashable
    """Name of the field."""

    data: ArraySpec
    """Data specification of the field."""


@dataclass(frozen=True)
class ScalarFieldSpec:
    """Specification of scalar fields."""

    type: Literal["attr", "name"]
    """Type of the field."""

    name: Hashable
    """Name of the field."""

    data: ScalarSpec
    """Data specification of the field."""


class FieldSpecs(Dict[str, AnyFieldSpec]):
    """Specifications of the dataclass fields."""

    @property
    def of_attr(self) -> Dict[str, ScalarFieldSpec]:
        """Select specifications of the attribute fields."""
        return {k: v for k, v in self.items() if v.type == "attr"}

    @property
    def of_data(self) -> Dict[str, ArrayFieldSpec]:
        """Select specifications of the data fields."""
        return {k: v for k, v in self.items() if v.type == "data"}

    @property
    def of_index(self) -> Dict[str, ArrayFieldSpec]:
        """Select specifications of the index fields."""
        return {k: v for k, v in self.items() if v.type == "index"}

    @property
    def of_name(self) -> Dict[str, ScalarFieldSpec]:
        """Select specifications of the name fields."""
        return {k: v for k, v in self.items() if v.type == "name"}


@dataclass(frozen=True)
class DataSpec:
    """Specification of pandas dataclasses."""

    fields: FieldSpecs = field(default_factory=FieldSpecs)
    """Specifications of the dataclass fields."""

    @classmethod
    def from_dataclass(cls, dataclass: Type[DataClass]) -> "DataSpec":
        """Create a specification from a dataclass."""
        dataspec = cls()

        for field in fields(eval_fields(dataclass)):
            fieldspec = get_fieldspec(field)

            if fieldspec is not None:
                dataspec.fields[field.name] = fieldspec

        return dataspec


# runtime functions
@lru_cache(maxsize=None)
def eval_fields(dataclass: Type[TDataClass]) -> Type[TDataClass]:
    """Evaluate types of dataclass fields."""
    types = get_type_hints(dataclass, include_extras=True)

    for field in fields(dataclass):
        field.type = types[field.name]

    return dataclass


@lru_cache(maxsize=None)
def get_fieldspec(field: AnyField) -> Optional[AnyFieldSpec]:
    """Parse a dataclass field and return a field specification."""
    ftype = get_ftype(field.type)
    name = get_name(field.type, field.name)

    if ftype is FType.DATA or ftype is FType.INDEX:
        return ArrayFieldSpec(
            type=ftype.value,
            name=name,
            data=ArraySpec(get_dtype(field.type), field.default),
        )

    if ftype is FType.ATTR or ftype is FType.NAME:
        return ScalarFieldSpec(
            type=ftype.value,
            name=name,
            data=ScalarSpec(get_annotated(field.type), field.default),
        )
