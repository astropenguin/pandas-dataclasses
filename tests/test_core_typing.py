# standard library
from typing import Any, Hashable, List, Literal as L, Optional, Tuple, Union


# dependencies
import numpy as np
import pandas as pd
from pandas_dataclasses import Attr, Column, Data, Index
from pandas_dataclasses.core.specs import get_dtype, get_first
from pytest import mark
from typing_extensions import Annotated as Ann


# test data
testdata_dtype: List[Tuple[Any, Any]] = [
    (Data[Any], None),
    (Data[None], None),
    (Data[int], np.dtype("i8")),
    (Data[Union[int, None]], np.dtype("i8")),
    (Data[L["i8"]], np.dtype("i8")),
    (Data[L["boolean"]], pd.BooleanDtype()),
    (Data[L["category"]], pd.CategoricalDtype()),
    (Index[Any], None),
    (Index[None], None),
    (Index[int], np.dtype("i8")),
    (Index[Union[int, None]], np.dtype("i8")),
    (Index[L["i8"]], np.dtype("i8")),
    (Index[L["boolean"]], pd.BooleanDtype()),
    (Index[L["category"]], pd.CategoricalDtype()),
    (Ann[Data[float], "data"], np.dtype("f8")),
    (Ann[Index[float], "index"], np.dtype("f8")),
    (Union[Ann[Data[float], "data"], Ann[Any, "any"]], np.dtype("f8")),
    (Union[Ann[Index[float], "index"], Ann[Any, "any"]], np.dtype("f8")),
]

testdata_first: List[Tuple[Any, Optional[Hashable]]] = [
    (Attr[Any], None),  # type: ignore
    (Column[Any], None),  # type: ignore
    (Data[Any], None),
    (Index[Any], None),
    (Any, None),
    (Ann[Attr[Any], "attr"], "attr"),  # type: ignore
    (Ann[Column[Any], "column"], "column"),  # type: ignore
    (Ann[Data[Any], "data"], "data"),
    (Ann[Index[Any], "index"], "index"),
    (Ann[Any, "other"], None),
    (Ann[Attr[Any], ..., "attr"], None),  # type: ignore
    (Ann[Column[Any], ..., "column"], None),  # type: ignore
    (Ann[Data[Any], ..., "data"], None),
    (Ann[Index[Any], ..., "index"], None),
    (Ann[Any, ..., "other"], None),
    (Union[Ann[Attr[Any], "attr"], Ann[Any, "any"]], "attr"),  # type: ignore
    (Union[Ann[Column[Any], "column"], Ann[Any, "any"]], "column"),  # type: ignore
    (Union[Ann[Data[Any], "data"], Ann[Any, "any"]], "data"),
    (Union[Ann[Index[Any], "index"], Ann[Any, "any"]], "index"),
    (Union[Ann[Any, "other"], Ann[Any, "any"]], None),
]


# test functions
@mark.parametrize("tp, dtype", testdata_dtype)
def test_get_dtype(tp: Any, dtype: Optional[str]) -> None:
    assert get_dtype(tp) == dtype


@mark.parametrize("tp, first", testdata_first)
def test_get_first(tp: Any, first: Optional[Any]) -> None:
    assert get_first(tp, None) == first
