__all__ = ["DataSpec"]


# standard library
from dataclasses import MISSING, Field, dataclass, field, fields
from functools import lru_cache
from typing import Any, Dict, Hashable, List, Optional, Type, TypeVar, Union


# dependencies
import numpy as np
from typing_extensions import Literal, get_type_hints


# submodules
from .typing import DataClass, FieldType, deannotate, get_dtype, get_ftype, get_name


# type hints
FieldSpec = Union["ArrayFieldSpec", "ScalarFieldSpec"]
TDataClass = TypeVar("TDataClass", bound=DataClass)


# runtime classes
@dataclass(frozen=True)
class ArraySpec:
    """Specification of arrays."""

    type: Optional["np.dtype[Any]"]
    """Data type of the array."""

    default: Any
    """Default value of the array."""

    def __call__(self, obj: Any = MISSING) -> "np.ndarray[Any, Any]":
        """Convert an object be spec-compliant."""
        if obj is MISSING:
            obj = self.default

        if obj is MISSING:
            raise ValueError("Value is missing.")

        return np.asarray(obj, dtype=self.type)


@dataclass(frozen=True)
class ScalarSpec:
    """Specification of scalars."""

    type: Any
    """Type of the scalar."""

    default: Any
    """Default value of the scalar."""

    def __call__(self, obj: Any = MISSING) -> Any:
        """Convert an object be spec-compliant."""
        if obj is MISSING:
            obj = self.default

        if obj is MISSING:
            raise ValueError("Value is missing.")

        return obj


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


@dataclass(frozen=True)
class DataSpec:
    """Specification of pandas dataclasses."""

    fields: Dict[str, FieldSpec] = field(default_factory=dict)
    """Specifications of the dataclass fields."""

    @property
    def attrs(self) -> List[ScalarFieldSpec]:
        """Return specifications of the attribute fields."""
        return [v for v in self.fields.values() if v.type == "attr"]

    @property
    def data(self) -> List[ArrayFieldSpec]:
        """Return specifications of the data fields."""
        return [v for v in self.fields.values() if v.type == "data"]

    @property
    def indexes(self) -> List[ArrayFieldSpec]:
        """Return specifications of the index fields."""
        return [v for v in self.fields.values() if v.type == "index"]

    @property
    def names(self) -> List[ScalarFieldSpec]:
        """Return specifications of the name fields."""
        return [v for v in self.fields.values() if v.type == "name"]

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
        return ScalarFieldSpec(
            type=ftype.value,
            name=name,
            data=ScalarSpec(deannotate(field.type), field.default),
        )
