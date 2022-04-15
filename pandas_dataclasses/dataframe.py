# dependencies
from typing_extensions import ParamSpec, Protocol


# submodules
from .typing import DataClass


# type hints
PInit = ParamSpec("PInit")


class DataClass(DataClass, Protocol[PInit]):
    """Type hint for dataclass objects (with parameter specification)."""

    def __init__(self, *args: PInit.args, **kwargs: PInit.kwargs) -> None:
        ...
