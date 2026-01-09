from __future__ import annotations
from .core import _Set
from .data import PMod

import numpy as np
import numbers, operator
from typing import Self, TypeAlias, Callable, Any, Literal
from collections.abc import Sequence, Iterator

Numeric = numbers.Real
ArrayLike: TypeAlias = '_Set | Sequence[Numeric]'
Index = int | slice | Sequence[int] | np.ndarray

class _PSet(_Set):
    
    # TODO
    # conversioni:
    #   - frequenze
    #   - midi
    #   - simboli Lily
    # intervalli (semantica deltas)
    # intervalli gradi funzionali

    def __init__(self, values: ArrayLike, offset: Numeric = 0) -> None:
        super().__init__(values, offset)
        
    def intervals(self, *, reference: Numeric = 0) -> list[Numeric]:
        if reference != 0:
            return self.vals - reference
        else:
            return self.deltas
    
    def to_freq(self, a4: float = 440.0) -> list[float]:
        return (a4 * (2 ** ((self.vals - 69) / 12))).tolist()
    
    @classmethod
    def from_freq(cls, freqs: list[float], a4: float = 440.0) -> _PSet:
        return cls(69 + 12 * np.log2(np.array(freqs) / a4))

class Scale(_PSet):

    def __init__(self, intervals: ArrayLike, root: Numeric = 0, scale_harmo: ArrayLike = None) -> None:
        super().__init__(intervals, offset=root)
        self.chords = scale_harmo

    @classmethod
    def new(cls, model: PMod, root: int = 60) -> Scale:
        return cls(model['intervals'], model['scale_harmo'], root=root)

class Chord(_PSet):
    
    pass