from __future__ import annotations
from .pitch import Chord, Scale

import numpy as np
import numbers
from typing import Self
from collections.abc import Sequence

Numeric = numbers.Real
ArrayLike = Sequence[Numeric]
Index = int | slice | Sequence[int]


class PitchSequence:

    def __init__(self, note_sequence: tuple) -> None:

        '''
        Order Sequence of pitches 
        
        :param note_sequence: list of Chord, Scale or single notes
        :type note_sequence: tuple

        Example:
        >>> a = PitchSequence((60, Chord([1, 2, 3], 50), Scale.new(ScaleModel.maj, 60)))
        >>> print(a)
        PitchSequence = [60, Chord = [51, 52, 53], Scale = [60, 62, 64, 65, 67, 69, 71]]
        '''
        
        self.seq = []               # tuple di istanze o liste in input
        self.note = []              # array di note o accordi da stampare

        for i in range(len(note_sequence)):
            idItem = (i, note_sequence[i])
            
            if isinstance(idItem[1], list):
                for j in idItem[1]:
                    self.seq.append(j)
            else:
                self.seq.append(idItem[1])
                    

    def __iter__(self):
        return (v for v in self.seq)
    
    def __len__(self) -> int:
        return len(self.seq)
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__} = {self.seq}'
    
    def __getitem__(self, key: Index) -> Chord | Scale | Numeric:
        return self.seq[key]

    def __setitem__(self, key: Index, value):
        self.seq[key] = value
        return self

    @property
    def out(self):
        '''
        Return the order list

        Example:
        >>> a = PitchSequence((60, Chord([1, 2, 3], 50), Scale.new(ScaleModel.maj, 60)))
        >>> print(a.out)
        [60, [51, 52, 53], 60, 62, 64, 65, 67, 69, 71]
        '''
        for i in self.seq:

            if isinstance(i, list):
                for j in i:
                    if isinstance(j, (int, float)):
                        self.note.append(j)
                    elif isinstance(j, Scale):
                        self.note += j.pitches
                    elif isinstance(j, Chord):
                        self.note.append(j.pitches)
            elif isinstance(i, (int, float)):
                self.note.append(i)
            elif isinstance(i, Scale):
                self.note += i.pitches
            elif isinstance(i, Chord):
                self.note.append(i.pitches)

        return self.note