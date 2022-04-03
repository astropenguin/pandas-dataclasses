__all__ = ["DataSpec"]


# standard library
from dataclasses import dataclass, field
from typing import Any, Dict, Hashable, Optional, Union


# dependencies
import numpy as np
from typing_extensions import Literal


# type hints
AnyField = Union["ArrayField", "MetaField"]


# runtime classes
class MissingType:
    """Singleton that indicates missing data."""

    def __repr__(self) -> str:
        return "<MISSING>"


MISSING = MissingType()


@dataclass(frozen=True)
class Array:
    """Specifications for arrays."""

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
class Meta:
    """Specifications for metadata."""

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
class ArrayField:
    """Specifications for array fields."""

    type: Literal["attr", "name"]
    """Type of the field."""

    name: Hashable
    """Name of the field."""

    data: Array
    """Data specifications of the field."""


@dataclass(frozen=True)
class MetaField:
    """Specifications for metadata fields."""

    type: Literal["attr", "name"]
    """Type of the field."""

    name: Hashable
    """Name of the field."""

    data: Meta
    """Data specifications of the field."""


@dataclass(frozen=True)
class DataSpec:
    """Specifications for pandas dataclasses."""

    fields: Dict[str, AnyField] = field(default_factory=dict)
    """Field specifications of the dataclass."""
