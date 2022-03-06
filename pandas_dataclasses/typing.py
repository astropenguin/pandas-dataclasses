__all__ = ["Data", "Index", "NamedData", "NamedIndex"]


# standard library
from enum import Enum
from typing import Any, Collection, Hashable, Optional, TypeVar, Union


# dependencies
from typing_extensions import (
    Annotated,
    Literal,
    Protocol,
    get_args,
    get_origin,
    get_type_hints,
)


# type hints (private)
TDtype = TypeVar("TDtype", covariant=True)
TName = TypeVar("TName", bound=Hashable, covariant=True)


class Named(Protocol[TName]):
    pass


class Collection(Named[TName], Collection[TDtype], Protocol):
    pass


# type hints (public)
class FieldType(Enum):
    DATA = "data"
    INDEX = "index"

    def annotates(self, hint: Any) -> bool:
        return self in get_args(hint)[1:]


Data = Annotated[Union[Collection[None, TDtype], TDtype], FieldType.DATA]
Index = Annotated[Union[Collection[None, TDtype], TDtype], FieldType.INDEX]
NamedData = Annotated[Union[Collection[TName, TDtype], TDtype], FieldType.DATA]
NamedIndex = Annotated[Union[Collection[TName, TDtype], TDtype], FieldType.INDEX]


# runtime functions
def get_dtype(type_: Any) -> Optional[str]:
    args = get_args(type_)
    origin = get_origin(type_)

    if origin is Collection:
        return get_dtype(args[1])

    if origin is Literal:
        return args[0]

    if type_ is Any or type_ is type(None):
        return None

    if isinstance(type_, type):
        return type_.__name__

    raise ValueError(f"Could not convert {type_!r} to dtype.")


def get_ftype(type_: Any) -> FieldType:
    if FieldType.DATA.annotates(type_):
        return FieldType.DATA

    if FieldType.INDEX.annotates(type_):
        return FieldType.INDEX

    raise ValueError(f"Could not convert {type_!r} to ftype.")


def get_name(type_: Any) -> Optional[Hashable]:
    args = get_args(type_)
    origin = get_origin(type_)

    if origin is Collection:
        return get_dtype(args[0])

    if origin is Literal:
        return args[0]

    if type_ is type(None):
        return None

    raise ValueError(f"Could not convert {type_!r} to name.")


def get_rtype(type_: Any) -> Any:
    class Temporary:
        __annotations__ = dict(type=type_)

    try:
        unannotated = get_type_hints(Temporary)["type"]
    except NameError:
        raise ValueError(f"Could not convert {type_!r} to rtype.")

    if get_origin(unannotated) is Union:
        return get_args(unannotated)[0]
    else:
        return unannotated
