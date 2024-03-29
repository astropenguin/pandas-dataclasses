# standard library
from typing import Any, Union


# dependencies
from pandas_dataclasses import Attr, Data, Index, Tag
from pandas_dataclasses.core.tagging import get_tags
from pytest import mark
from typing_extensions import Annotated as Ann


# test data
testdata: list[tuple[Any, tuple[Tag, ...]]] = [
    (Attr[Any], (Tag.ATTR,)),  # type: ignore
    (Data[Any], (Tag.DATA,)),
    (Index[Any], (Tag.INDEX,)),
    (Any, ()),
    (Ann[Attr[Any], "attr"], (Tag.ATTR,)),  # type: ignore
    (Ann[Data[Any], "data"], (Tag.DATA,)),
    (Ann[Index[Any], "index"], (Tag.INDEX,)),
    (Ann[Any, "other"], ()),
    (Union[Ann[Attr[Any], "attr"], Ann[Any, "any"]], (Tag.ATTR,)),  # type: ignore
    (Union[Ann[Data[Any], "data"], Ann[Any, "any"]], (Tag.DATA,)),
    (Union[Ann[Index[Any], "index"], Ann[Any, "any"]], (Tag.INDEX,)),
    (Union[Ann[Any, "other"], Ann[Any, "any"]], ()),
]


# test functions
@mark.parametrize("tp, tags", testdata)
def test_get_tags(tp: Any, tags: tuple[Tag, ...]) -> None:
    assert get_tags(tp) == tags
