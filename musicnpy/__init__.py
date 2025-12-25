"""
musicnpy
========

A collection of functions and classes for assisted composition. Thanks to NumPy, it remains computationally efficient and versatile at a high level.

Submodules
----------
- core
- pitch
- durs
- velo
- topyly
"""

# Import principale
from .core import _Set
from .pitch import _PSet, Scale
from .topyly import Staff, _Voice, _Print, _Map, Score

# Definisce cosa viene esportato con 'from musicnpy import *'
__all__ = ["_Set", "_PSet", "Scale", "Staff", "_Voice", "_Print", "_Map", "Score"]