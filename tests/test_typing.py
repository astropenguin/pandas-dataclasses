# standard library
from typing import Any, Collection, Optional, Union


# dependencies
from pytest import mark
from typing_extensions import Annotated, Literal


# submodules
from pandas_dataclasses.typing import (
    Attr,
    Data,
    Index,
    Name,
    get_dtype,
    get_ftype,
    get_rtype,
)


# type hints
Int64 = Literal["int64"]
NoneType = type(None)


# test datasets
testdata_dtype = [
    (Any, None),
    (NoneType, None),
    (Int64, "int64"),
    (int, "int"),
    (Collection[Any], None),
    (Collection[None], None),
    (Collection[Int64], "int64"),
    (Collection[int], "int"),
]

testdata_ftype = [
    (Attr[Any], "attr"),
    (Data[Any], "data"),
    (Index[Any], "index"),
    (Name[Any], "name"),
]

testdata_rtype = [
    (int, int),
    (Annotated[int, "annotation"], int),
    (Union[int, float], int),
    (Optional[int], int),
]


# test functions
@mark.parametrize("type_, dtype", testdata_dtype)
def test_get_dtype(type_: Any, dtype: Any) -> None:
    assert get_dtype(type_) == dtype


@mark.parametrize("type_, ftype", testdata_ftype)
def test_get_field_type(type_: Any, ftype: Any) -> None:
    assert get_ftype(type_).value == ftype


@mark.parametrize("type_, rtype", testdata_rtype)
def test_get_rtype(type_: Any, rtype: Any) -> None:
    assert get_rtype(type_) == rtype
