__author__ = "Akio Taniguchi <taniguchi@a.phys.nagoya-u.ac.jp>"
__version__ = "0.2.0"


# submodules
from . import core  # type: ignore
from . import specs  # type: ignore
from . import typing  # type: ignore


# subpackages
from . import pandas  # type: ignore


# aliases
from .core import *
from .pandas import *
from .specs import *
from .typing import *
