# standard library
from dataclasses import dataclass
from typing import Any, Optional


# dependencies
import numpy as np


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
class Metadata:
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
