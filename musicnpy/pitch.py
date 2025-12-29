from __future__ import annotations
from .core import _Set

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
    # ottava +/- 1 o più se specificato
    # ottava specifica
    # intervalli (semantica deltas)
    # intervalli gradi funzionali

    def __init__(self, list, offset = 0):
        super().__init__(list, offset)

    def intervals(self, *, reference: Numeric = None) -> list[Numeric]:
        if reference is not None:
            return self.vals - reference
        else:
            return self.deltas
    
    def to_freq(self, a4: float = 440.0) -> list[float]:
        return (a4 * (2 ** ((self.vals - 69) / 12))).tolist()
    
    @classmethod
    def from_freq(cls, freqs: list[float], a4: float = 440.0) -> list[float]:
        return cls(69 + 12 * np.log2(np.array(freqs) / a4))

class Scale(_PSet):

    pass