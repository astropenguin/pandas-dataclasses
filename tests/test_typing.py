# standard library
from typing import Any


# dependencies
import numpy as np
from pytest import mark
from typing_extensions import Literal


# submodules
from pandas_dataclasses.typing import (
    Attr,
    Data,
    Index,
    Name,
    Named,
    get_dtype,
    get_ftype,
    get_name,
)


# test datasets
testdata_dtype = [
    (Data[Any], None),
    (Data[None], None),
    (Data[int], np.dtype("int64")),
    (Data[Literal["i8"]], np.dtype("int64")),
    (Index[Any], None),
    (Index[None], None),
    (Index[int], np.dtype("int64")),
    (Index[Literal["i8"]], np.dtype("int64")),
]

testdata_ftype = [
    (Attr[Any], "attr"),
    (Data[Any], "data"),
    (Index[Any], "index"),
    (Name[Any], "name"),
    (Any, "other"),
]

testdata_name = [
    (Attr[Any], None),
    (Data[Any], None),
    (Index[Any], None),
    (Name[Any], None),
    (Named[Attr[Any], "attr"], "attr"),
    (Named[Data[Any], "data"], "data"),
    (Named[Index[Any], "index"], "index"),
    (Named[Name[Any], "name"], "name"),
]

# test functions
@mark.parametrize("type_, dtype", testdata_dtype)
def test_get_dtype(type_: Any, dtype: Any) -> None:
    assert get_dtype(type_) == dtype


@mark.parametrize("type_, ftype", testdata_ftype)
def test_get_ftype(type_: Any, ftype: Any) -> None:
    assert get_ftype(type_).value == ftype


@mark.parametrize("type_, name", testdata_name)
def test_get_name(type_: Any, name: Any) -> None:
    assert get_name(type_) == name
