# standard library
from typing import Any


# dependencies
import numpy as np
from pytest import mark
from typing_extensions import Literal


# submodules
from pandas_dataclasses.typing import Attr, Data, Index, Name, get_dtype, get_ftype


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
]

# test functions
@mark.parametrize("type_, dtype", testdata_dtype)
def test_get_dtype(type_: Any, dtype: Any) -> None:
    assert get_dtype(type_) == dtype


@mark.parametrize("type_, ftype", testdata_ftype)
def test_get_ftype(type_: Any, ftype: Any) -> None:
    assert get_ftype(type_).value == ftype
