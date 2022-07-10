__all__ = ["DataSpec"]


# standard library
from dataclasses import dataclass, field, fields
from functools import lru_cache
from typing import Any, Dict, Optional, Type


# dependencies
from typing_extensions import Literal, TypeAlias, get_type_hints


# submodules
from .typing import (
    AnyDType,
    AnyField,
    AnyName,
    AnyPandas,
    DataClass,
    P,
    Role,
    get_annotated,
    get_dtype,
    get_name,
    get_role,
)


# type hints
AnySpec: TypeAlias = "ArraySpec | ScalarSpec"


# runtime classes
@dataclass(frozen=True)
class ArraySpec:
    """Specification of an array."""

    name: AnyName
    """Name of the array."""

    role: Literal["data", "index"]
    """Role of the array."""

    dtype: Optional[AnyDType]
    """Data type of the array."""

    default: Any
    """Default value of the array."""


@dataclass(frozen=True)
class ScalarSpec:
    """Specification of a scalar."""

    name: AnyName
    """Name of the scalar."""

    role: Literal["attr", "name"]
    """Role of the scalar."""

    type: Any
    """Type (hint) of the scalar."""

    default: Any
    """Default value of the scalar."""


class Specs(Dict[str, AnySpec]):
    """Dictionary of any specifications."""

    @property
    def of_attr(self) -> Dict[str, ScalarSpec]:
        """Limit to attribute specifications."""
        return {k: v for k, v in self.items() if v.role == "attr"}

    @property
    def of_data(self) -> Dict[str, ArraySpec]:
        """Limit to data specifications."""
        return {k: v for k, v in self.items() if v.role == "data"}

    @property
    def of_index(self) -> Dict[str, ArraySpec]:
        """Limit to index specifications."""
        return {k: v for k, v in self.items() if v.role == "index"}

    @property
    def of_name(self) -> Dict[str, ScalarSpec]:
        """Limit to name specifications."""
        return {k: v for k, v in self.items() if v.role == "name"}


@dataclass(frozen=True)
class DataSpec:
    """Data specification of a pandas dataclass."""

    factory: Optional[Type[AnyPandas]] = None
    """Factory for pandas data creation."""

    specs: Specs = field(default_factory=Specs)
    """Dictionary of any specifications."""

    @classmethod
    def from_dataclass(cls, dataclass: Type[DataClass[P]]) -> "DataSpec":
        """Create a data specification from a dataclass."""
        specs = Specs()

        for field in fields(eval_types(dataclass)):
            spec = get_spec(field)

            if spec is not None:
                specs[field.name] = spec

        factory = getattr(dataclass, "__pandas_factory__", None)
        return cls(factory, specs)


# runtime functions
@lru_cache(maxsize=None)
def eval_types(dataclass: Type[DataClass[P]]) -> Type[DataClass[P]]:
    """Evaluate field types of a dataclass."""
    types = get_type_hints(dataclass, include_extras=True)

    for field in fields(dataclass):
        field.type = types[field.name]

    return dataclass


@lru_cache(maxsize=None)
def get_spec(field: AnyField) -> Optional[AnySpec]:
    """Convert a dataclass field to a specification."""
    name = get_name(field.type, field.name)
    role = get_role(field.type)

    if role is Role.DATA or role is Role.INDEX:
        return ArraySpec(
            name=name,
            role=role.value,
            dtype=get_dtype(field.type),
            default=field.default,
        )

    if role is Role.ATTR or role is Role.NAME:
        return ScalarSpec(
            name=name,
            role=role.value,
            type=get_annotated(field.type),
            default=field.default,
        )
