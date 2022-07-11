# standard library
from typing import Any, Union


# dependencies
import numpy as np
import pandas as pd
from pytest import mark
from typing_extensions import Annotated as Ann
from typing_extensions import Literal as L
from pandas_dataclasses.core.typing import (
    Attr,
    Data,
    Index,
    Name,
    Role,
    get_dtype,
    get_name,
    get_role,
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
    (Ann[Attr[Any], dict(name="attr")], dict(name="attr")),
    (Ann[Data[Any], dict(name="data")], dict(name="data")),
    (Ann[Index[Any], dict(name="index")], dict(name="index")),
    (Ann[Name[Any], dict(name="name")], dict(name="name")),
    (Ann[Any, "other"], None),
    (Union[Ann[Attr[Any], "attr"], Ann[Any, "any"]], "attr"),
    (Union[Ann[Data[Any], "data"], Ann[Any, "any"]], "data"),
    (Union[Ann[Index[Any], "index"], Ann[Any, "any"]], "index"),
    (Union[Ann[Name[Any], "name"], Ann[Any, "any"]], "name"),
    (Union[Ann[Any, "other"], Ann[Any, "any"]], None),
]

testdata_role = [
    (Attr[Any], Role.ATTR),
    (Data[Any], Role.DATA),
    (Index[Any], Role.INDEX),
    (Name[Any], Role.NAME),
    (Any, Role.OTHER),
    (Ann[Attr[Any], "attr"], Role.ATTR),
    (Ann[Data[Any], "data"], Role.DATA),
    (Ann[Index[Any], "index"], Role.INDEX),
    (Ann[Name[Any], "name"], Role.NAME),
    (Ann[Any, "other"], Role.OTHER),
    (Union[Ann[Attr[Any], "attr"], Ann[Any, "any"]], Role.ATTR),
    (Union[Ann[Data[Any], "data"], Ann[Any, "any"]], Role.DATA),
    (Union[Ann[Index[Any], "index"], Ann[Any, "any"]], Role.INDEX),
    (Union[Ann[Name[Any], "name"], Ann[Any, "any"]], Role.NAME),
    (Union[Ann[Any, "other"], Ann[Any, "any"]], Role.OTHER),
]


# test functions
@mark.parametrize("tp, dtype", testdata_dtype)
def test_get_dtype(tp: Any, dtype: Any) -> None:
    assert get_dtype(tp) == dtype


@mark.parametrize("tp, name", testdata_name)
def test_get_name(tp: Any, name: Any) -> None:
    assert get_name(tp) == name


@mark.parametrize("tp, role", testdata_role)
def test_get_role(tp: Any, role: Any) -> None:
    assert get_role(tp) is role
