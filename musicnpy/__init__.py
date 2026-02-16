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
- data
- collections
- topyly
"""
__version__ = "0.1.0"
# Import principale
from .core import _Set
from .pitch import _PSet, Scale, Chord
from .durs import Pattern, grid
from .data import ScaleModel, ChordModel
from .collections import PitchSequence
from .topyly import Staff, _Voice, _Print, _Map, Score, nDim

# # Definisce cosa viene esportato con 'from musicnpy import *'
__all__ = [
    "_Set", 
    "_PSet", 
    "Scale",
    "Chord",
    "PitchSequence",
    "Staff", 
    "_Voice", 
    "_Print", 
    "_Map", 
    "Score", 
    "ScaleModel",
    "ChordModel",
    "Pattern",
    "grid",
    "nDim"
]

# from musicnpy import *