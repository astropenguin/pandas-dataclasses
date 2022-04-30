__author__ = "Akio Taniguchi <taniguchi@a.phys.nagoya-u.ac.jp>"
__version__ = "0.1.0"


# submodules
from . import specs  # type: ignore
from . import typing  # type: ignore


# subpackages
from . import pandas  # type: ignore


# aliases
from .pandas import *
from .specs import *
from .typing import *
