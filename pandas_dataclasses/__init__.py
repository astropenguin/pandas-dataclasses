__all__ = [
    "As",
    "AsDataFrame",
    "AsFrame",
    "AsSeries",
    "Attr",
    "Column",
    "Data",
    "Index",
    "Other",
    "Spec",
    "asdataframe",
    "asframe",
    "asseries",
    "core",
]


from . import core
from .core.aspandas import *
from .core.mixins import *
from .core.specs import *
from .core.typing import *


# metadata
__version__ = "0.8.0"


# aliases
AsDataFrame = AsFrame
"""Alias of ``core.mixins.AsFrame``."""


asdataframe = asframe
"""Alias of ``core.aspandas.asframe``."""
