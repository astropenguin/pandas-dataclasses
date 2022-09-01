__all__ = ["Attr", "Column", "Data", "Index", "Other"]


# standard library
from dataclasses import Field
from enum import Enum, auto
from itertools import chain
from typing import (
    Any,
    ClassVar,
    Collection,
    Hashable,
    Iterable,
    Optional,
    Tuple,
    Type,
    TypeVar,
)


# dependencies
import pandas as pd
from pandas.api.types import pandas_dtype  # type: ignore
from typing_extensions import (
    Annotated,
    Literal,
    ParamSpec,
    Protocol,
    TypeAlias,
    get_args,
    get_origin,
    get_type_hints,
)


# type hints (private)
AnyPandas: TypeAlias = "pd.DataFrame | pd.Series"
P = ParamSpec("P")
T = TypeVar("T")
THashable = TypeVar("THashable", bound=Hashable)
TPandas = TypeVar("TPandas", bound=AnyPandas)


class DataClass(Protocol[P]):
    """Type hint for dataclass objects."""

    __dataclass_fields__: ClassVar["dict[str, Field[Any]]"]

    def __init__(self, *args: P.args, **kwargs: P.kwargs) -> None:
        ...


class PandasClass(DataClass[P], Protocol[P, TPandas]):
    """Type hint for dataclass objects with a pandas factory."""

    __pandas_factory__: Type[TPandas]


class Role(Enum):
    """Annotations for typing dataclass fields."""

    ATTR = auto()
    """Annotation for attribute fields."""

    COLUMN = auto()
    """Annotation for column fields."""

    DATA = auto()
    """Annotation for data fields."""

    INDEX = auto()
    """Annotation for index fields."""

    OTHER = auto()
    """Annotation for other fields."""

    @classmethod
    def annotates(cls, tp: Any) -> bool:
        """Check if any role annotates a type hint."""
        return any(isinstance(arg, cls) for arg in get_args(tp))


# type hints (public)
Attr = Annotated[T, Role.ATTR]
"""Type hint for attribute fields (``Attr[T]``)."""

Column = Annotated[T, Role.COLUMN]
"""Type hint for column fields (``Column[T]``)."""

Data = Annotated[Collection[T], Role.DATA]
"""Type hint for data fields (``Data[T]``)."""

Index = Annotated[Collection[T], Role.INDEX]
"""Type hint for index fields (``Index[T]``)."""

Other = Annotated[T, Role.OTHER]
"""Type hint for other fields (``Other[T]``)."""


# runtime functions
def deannotate(tp: Any) -> Any:
    """Recursively remove annotations in a type hint."""

    class Temporary:
        __annotations__ = dict(tp=tp)

    return get_type_hints(Temporary)["tp"]


def find_annotated(tp: Any) -> Iterable[Any]:
    """Generate all annotated types in a type hint."""
    args = get_args(tp)

    if get_origin(tp) is Annotated:
        yield tp
        yield from find_annotated(args[0])
    else:
        yield from chain(*map(find_annotated, args))


def get_annotated(tp: Any) -> Any:
    """Extract the first role-annotated type."""
    for annotated in filter(Role.annotates, find_annotated(tp)):
        return deannotate(annotated)

    raise TypeError("Could not find any role-annotated type.")


def get_annotations(tp: Any) -> Tuple[Any, ...]:
    """Extract annotations of the first role-annotated type."""
    for annotated in filter(Role.annotates, find_annotated(tp)):
        return get_args(annotated)[1:]

    raise TypeError("Could not find any role-annotated type.")


def get_dtype(tp: Any) -> Optional[str]:
    """Extract a NumPy or pandas data type."""
    try:
        dtype = get_args(get_annotated(tp))[0]
    except (IndexError, TypeError):
        return

    if dtype is Any or dtype is type(None):
        return

    if get_origin(dtype) is Literal:
        dtype = get_args(dtype)[0]

    return pandas_dtype(dtype).name


def get_name(tp: Any, default: Hashable = None) -> Hashable:
    """Extract a name if found or return given default."""
    try:
        name = get_annotations(tp)[1]
    except (IndexError, TypeError):
        return default

    try:
        hash(name)
    except TypeError:
        raise ValueError("Could not find any valid name.")

    return name


def get_role(tp: Any, default: Role = Role.OTHER) -> Role:
    """Extract a role if found or return given default."""
    try:
        return get_annotations(tp)[0]
    except TypeError:
        return default
