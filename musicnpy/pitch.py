from __future__ import annotations
from .core import _Set, pad
from .data import ScaleModel, ChordModel

import numpy as np
import numbers
from typing import Self
from collections.abc import Sequence

Numeric = numbers.Real
ArrayLike = Sequence[Numeric]
Index = int | slice | Sequence[int]


class _PSet(_Set):
    
    """
    Utilities for future pitch class
    TODO implementare quantizzazione a quarti di tono
    """

    def __init__(self, values: ArrayLike, offset: Numeric) -> None:
        """
        Representation of a list of notes
        
        :param values: Notes.
        :type values: ArrayLike
        :param offset: Offset for the notes.
        :type offset: Numeric
        """
        super().__init__(values, offset)

    @property
    def pitches(self) -> list[Numeric]:
        """
        Return the absolute pitches in MIDI format.
        
        :return: list of pitches
        :rtype: list[Numeric]
        """
        return self.values

    @property
    def intervals(self) -> list[Numeric]:
        """
        Returns the intervals of the sequence. 
        NB: need the root note!!
        
        :return: list of intervals
        :rtype: list[Numeric]
        """
        return (self.vals - self.offset).tolist()
    
    @property
    def root(self) -> int:
        """
        Return the root note
        
        :return: root note
        :rtype: int
        """
        return self.offset
    
    def to_freq(self, A4: float = 440) -> list[float]:
        """
        Convert midi pitches in frequency
        
        :param A4: A4 tuning in frequence
        :type A4: float
        :return: list of frequencies
        :rtype: list[float]
        """
        return (A4 * (2 ** ((self.vals - 69) / 12))).tolist()
    
    @classmethod
    def from_freq(cls, freqs: list[float], a4: float = 440.0) -> Self:
        """
        Create new pitch class form list of frequencies

        :param freqs: list of frequencies
        :type freqs: list[float]
        :param a4: A4 tuning in frequence
        :type a4: float
        :return: new pitch istance
        :rtype: Self
        """
        frequenze = np.array(freqs)
        note = pow(440 * 2, (frequenze - 69)/12)
        print(note)
        return cls((69 + 12 * np.log2(np.array(freqs) / a4)).tolist())


class Scale(_PSet):

    chords: list[Chord]

    def __init__(self, intervals: ArrayLike, root: Numeric = 60, harmo: ArrayLike = None) -> None:
        """
        Rappresentation of a musicale Scale

        :param intervals: List of intervals
        :type intervals: ArrayLike
        :param root: Root note
        :type root: Numeric
        :param harmo: List of Chord class or ChordModel
        :type harmo: ArrayLike

        :Example:

        >>> a = Scale([0, 2, 4, 5, 7, 9, 11], 60)
        >>> print(a)
        Scale = [60, 62, 64, 65, 67, 69, 71]
        """
        super().__init__(intervals, offset=root)
        self.harmo = harmo
        self.chords = []

    @classmethod
    def new(cls, model: ScaleModel, root: int = 60) -> Scale:
        """
        Create a Scale from ScaleModel database

        :param model: scale model
        :type model: ScaleModel
        :param root: root note
        :type root: int
        :return: new istance
        :rtype: Scale

        :Example:

        >>> a = Scale.new(ScaleModel.maj, 60)
        >>> print(a)
        Scale = [60, 62, 63, 65, 67, 68, 70]
        """
        return cls(intervals=model['intervals'], root=root, harmo=model['harmo'])

    @property
    def diatonic(self) -> list[int]:
        """
        List of ints
        
        :return: Description
        :rtype: list[int]

        :Example:

        >>> a = Scale([0, 2, 3, 5, 7, 8, 10], 76)
        >>> print(a.diatonic)
        [1, 2, 3, 4, 5, 6, 7]
        """
        out = []
        for i in range(len(self)):
            out.append(i+1)
        return out

    @property
    def harmonize(self) -> list[Chord]:
        """
        List of chords fo the scale.
        
        :param self: Description
        :return: Description
        :rtype: list
        """
        if self.harmo != None:
            for i in enumerate(self):
                chordModel = self.harmo[i[0]]
                pitch = i[1]
                chord = Chord(notes=chordModel, root=pitch)
                self.chords.append(chord)
            return self.chords
        else:
            raise ValueError('Specify the harmo of scale')


class Chord(_PSet):

    def __init__(self, notes: ArrayLike = [0, 4, 7], root: Numeric = 0) -> None:
        """
        Rapresentation of Chord
        
        :param notes: List of intervals or pitches
        :type notes: ArrayLike
        :param root: Root note
        :type root: Numeric
        
        :Example:

        >>> a = Chord([0, 4, 7], 60) 
        >>> print(a)
        Chord = [60, 64, 67]
        """
        super().__init__(values=notes, offset=root)

    @classmethod
    def new(cls, model: ChordModel, root: Numeric = 0) -> Chord:
        """
        Create a Chord from ChordModel database
        
        :param model: ChordModel istance
        :type model: ChordModel
        :param root: Root note
        :type root: Numeric
        :return: new Chord instance
        :rtype: Chord

        :Example:

        >>> a = Chord.new(ChordModel.aug, 60)
        >>> print(a)
        Chord = [61, 65, 69]
        """
        return cls(notes = model, root = root)

    def n_inversion(self, pos: int) -> Self:
        """
        Inversion of chord
        
        :param pos: position of inversion
        :type pos: int
        :return: New Chord
        :rtype: Self

        :Example:

        >>> a = Chord([0, 1, 2, 3])
        >>> b = a.n_inversion(2)
        >>> print(b)
        Chord = [2, 3, 12, 13]
        """
        octaves = [12] * pos + [0] * (len(self) - pos)
        octaves = np.array(octaves)
        self.sort('<')
        return self.__class__((np.sort(self.vals + octaves)).tolist())

    @property
    def first_inv(self) -> Chord:
        """
        First inversion
        
        :return: New Chord
        :rtype: Chord

        :Example:
        
        >>> a = Chord.new(ChordModel.maj, 60)
        >>> b = a.first_inv
        >>> print(b)
        Chord = [64, 67, 72]
        """
        return self.n_inversion(1)

    @property
    def second_inv(self) -> Chord:
        """
        Second inversion
        
        :return: New Chord
        :rtype: Chord

        :Example:

        >>> a = Chord.new(ChordModel.maj, 60)
        >>> b = a.second_inv
        >>> print(b)
        Chord = [67, 72, 76]
        """
        return self.n_inversion(2)
    
    @property
    def acc(self) -> Chord:
        return Chord(self.pitches)
    #TODO arpeggi
    #TODO drop 2, drop 3 inversione dall'alto per Jazz nel databese ChordModel
    #TODO specificare in array l'inversione interna più irregolare [0, -1, 1, 0, 1], Octavazier
    #TODO specifica un range in cui portare il chord o scala, da fare in _PSet