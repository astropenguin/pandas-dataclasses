# standard library
from typing import Any, Union


# dependencies
import numpy as np
import pandas as pd
from pytest import mark
from typing_extensions import Annotated as Ann
from typing_extensions import Literal as L
from pandas_dataclasses.typing import (
    Attr,
    Data,
    FType,
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
    (Data[int], np.dtype("i8")),
    (Data[L["i8"]], np.dtype("i8")),
    (Data[L["boolean"]], pd.BooleanDtype()),
    (Data[L["category"]], pd.CategoricalDtype()),
    (Index[Any], None),
    (Index[None], None),
    (Index[int], np.dtype("i8")),
    (Index[L["i8"]], np.dtype("i8")),
    (Index[L["boolean"]], pd.BooleanDtype()),
    (Index[L["category"]], pd.CategoricalDtype()),
    (Ann[Data[float], "data"], np.dtype("f8")),
    (Ann[Index[float], "index"], np.dtype("f8")),
    (Union[Ann[Data[float], "data"], Ann[Any, "any"]], np.dtype("f8")),
    (Union[Ann[Index[float], "index"], Ann[Any, "any"]], np.dtype("f8")),
]

testdata_ftype = [
    (Attr[Any], FType.ATTR),
    (Data[Any], FType.DATA),
    (Index[Any], FType.INDEX),
    (Name[Any], FType.NAME),
    (Any, FType.OTHER),
    (Ann[Attr[Any], "attr"], FType.ATTR),
    (Ann[Data[Any], "data"], FType.DATA),
    (Ann[Index[Any], "index"], FType.INDEX),
    (Ann[Name[Any], "name"], FType.NAME),
    (Ann[Any, "other"], FType.OTHER),
    (Union[Ann[Attr[Any], "attr"], Ann[Any, "any"]], FType.ATTR),
    (Union[Ann[Data[Any], "data"], Ann[Any, "any"]], FType.DATA),
    (Union[Ann[Index[Any], "index"], Ann[Any, "any"]], FType.INDEX),
    (Union[Ann[Name[Any], "name"], Ann[Any, "any"]], FType.NAME),
    (Union[Ann[Any, "other"], Ann[Any, "any"]], FType.OTHER),
]

testdata_name = [
    (Attr[Any], None),
    (Data[Any], None),
    (Index[Any], None),
    (Name[Any], None),
    (Any, None),
    (Ann[Attr[Any], "attr"], "attr"),
    (Ann[Data[Any], "data"], "data"),
    (Ann[Index[Any], "index"], "index"),
    (Ann[Name[Any], "name"], "name"),
    (Ann[Any, "other"], None),
    (Union[Ann[Attr[Any], "attr"], Ann[Any, "any"]], "attr"),
    (Union[Ann[Data[Any], "data"], Ann[Any, "any"]], "data"),
    (Union[Ann[Index[Any], "index"], Ann[Any, "any"]], "index"),
    (Union[Ann[Name[Any], "name"], Ann[Any, "any"]], "name"),
    (Union[Ann[Any, "other"], Ann[Any, "any"]], None),
]


# test functions
@mark.parametrize("tp, dtype", testdata_dtype)
def test_get_dtype(tp: Any, dtype: Any) -> None:
    assert get_dtype(tp) == dtype


@mark.parametrize("tp, ftype", testdata_ftype)
def test_get_ftype(tp: Any, ftype: Any) -> None:
    assert get_ftype(tp) is ftype


@mark.parametrize("tp, name", testdata_name)
def test_get_name(tp: Any, name: Any) -> None:
    assert get_name(tp) == name
