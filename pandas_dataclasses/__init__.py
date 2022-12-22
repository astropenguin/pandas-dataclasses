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
    "aspandas",
    "asseries",
    "core",
    "extras",
]
__version__ = "0.11.0"


# submodules
from . import core
from . import extras
from .core.api import *
from .core.specs import *
from .core.typing import *
from .extras.new import *


# aliases
AsDataFrame = AsFrame
"""Alias of ``core.mixins.AsFrame``."""


asdataframe = asframe
"""Alias of ``core.aspandas.asframe``."""
