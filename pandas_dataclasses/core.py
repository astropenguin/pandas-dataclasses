__all__ = ["get_attrs"]


# standard library
from typing import Any, Dict, Hashable


# submodules
from .specs import DataSpec
from .typing import DataClass


# runtime functions
def get_attrs(obj: DataClass) -> Dict[Hashable, Any]:
    """Derive attributes from a dataclass object."""
    dataspec = DataSpec.from_dataclass(type(obj))
    attrs: Dict[Hashable, Any] = {}

    for key, spec in dataspec.fields.of_attr.items():
        attrs[spec.name] = getattr(obj, key)

    return attrs
