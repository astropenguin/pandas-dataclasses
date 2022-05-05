# standard library
from typing import Any, Optional, Union


# dependencies
import numpy as np
import pandas as pd
from pytest import mark
from typing_extensions import Annotated, Literal
from pandas_dataclasses.typing import (
    Attr,
    Data,
    Index,
    Name,
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
    (Data[Literal["boolean"]], pd.BooleanDtype()),
    (Index[Any], None),
    (Index[None], None),
    (Index[int], np.dtype("int64")),
    (Index[Literal["i8"]], np.dtype("int64")),
    (Index[Literal["boolean"]], pd.BooleanDtype()),
    (Optional[Data[float]], np.dtype("float64")),
    (Optional[Index[float]], np.dtype("float64")),
    (Union[Data[float], str], np.dtype("float64")),
    (Union[Index[float], str], np.dtype("float64")),
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
    (Annotated[Attr[Any], "attr"], "attr"),
    (Annotated[Data[Any], "data"], "data"),
    (Annotated[Index[Any], "index"], "index"),
    (Annotated[Name[Any], "name"], "name"),
]


# test functions
@mark.parametrize("tp, dtype", testdata_dtype)
def test_get_dtype(tp: Any, dtype: Any) -> None:
    assert get_dtype(tp) == dtype


@mark.parametrize("tp, ftype", testdata_ftype)
def test_get_ftype(tp: Any, ftype: Any) -> None:
    assert get_ftype(tp).value == ftype


@mark.parametrize("tp, name", testdata_name)
def test_get_name(tp: Any, name: Any) -> None:
    assert get_name(tp) == name
