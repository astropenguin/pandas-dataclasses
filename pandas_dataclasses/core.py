__all__ = ["get_attrs", "get_name"]


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


def get_name(obj: DataClass) -> Hashable:
    """Derive name from a dataclass object."""
    dataspec = DataSpec.from_dataclass(type(obj))

    for key in dataspec.fields.of_name.keys():
        return getattr(obj, key)
