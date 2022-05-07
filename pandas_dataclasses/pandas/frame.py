__all__ = ["asdataframe"]


# dependencies
import pandas as pd
from typing_extensions import ParamSpec, Protocol


# submodules
from ..core import get_attrs, get_data, get_index
from ..typing import DataClass


# type hints
PInit = ParamSpec("PInit")


class DataClass(DataClass, Protocol[PInit]):
    """Type hint for dataclass objects (with parameter specification)."""

    def __init__(self, *args: PInit.args, **kwargs: PInit.kwargs) -> None:
        ...


# runtime functions
def asdataframe(obj: DataClass[PInit]) -> pd.DataFrame:
    """Create a DataFrame object from a dataclass object."""
    attrs = get_attrs(obj)
    data = get_data(obj)
    index = get_index(obj)

    dataframe = pd.DataFrame(data, index)
    dataframe.attrs.update(attrs)
    return dataframe
