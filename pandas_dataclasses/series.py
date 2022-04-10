# standard library
from typing import List, Union


# dependencies
import pandas as pd
from typing_extensions import ParamSpec, Protocol


# submodules
from .typing import DataClass


# type hints
IndexLike = Union[List[pd.Index], pd.Index]
PInit = ParamSpec("PInit")


class DataClass(DataClass, Protocol[PInit]):
    """Type hint for dataclass objects (with parameter specification)."""

    def __init__(self, *args: PInit.args, **kwargs: PInit.kwargs) -> None:
        ...
