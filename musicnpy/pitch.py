from __future__ import annotations
from .core import _Set, pad
from .data import ScaleModel, ChordModel

import numpy as np
from math import log2
import numbers
from typing import Self
from collections.abc import Sequence

Numeric = numbers.Real
ArrayLike = Sequence[Numeric]
Index = int | slice | Sequence[int]



class _PSet(_Set):
    
    """
    Utilities for future pitch class
    """


    def __init__(self, values: ArrayLike, offset: Numeric) -> None:
        """
        Representation of a list of notes
        
        :param values: Notes.
        :type values: ArrayLike
        :param offset: Offset for the notes.
        :type offset: Numeric

        :Example:

        >>> a = _PSet([9, 0, 7, 1], 60)
        >>> print(a)
        _PSet = [69, 60, 67, 61]
        """
        super().__init__(values, offset)

    @property
    def pitches(self) -> list[Numeric]:
        """
        Return the absolute pitches in MIDI format.
        
        :return: list of pitches
        :rtype: list[Numeric]

        :Example:

        >>> a = _PSet([9, 0, 7, 1], 60)
        >>> print(a.pitches)
        [69, 60, 67, 61]
        """
        return self.values

    @property
    def intervals(self) -> list[Numeric]:
        """
        Returns the intervals of the sequence. 
        NB: need the root note!!
        
        :return: list of intervals
        :rtype: list[Numeric]

        :Example:

        >>> a = _PSet([9, 0, 7, 1], 60)
        >>> print(a.intervals)
        [9, 0, 7, 1]
        """
        return (self.vals - self.offset).tolist()
    
    @property
    def root(self) -> int:
        """
        Return the root note
        
        :return: root note
        :rtype: int

        :Example:

        >>> a = _PSet([9, 0, 7, 1], 60)
        >>> print(a.root)
        60
        """
        return self.offset
    
    def to_freq(self, A4: float = 440) -> list[float]:
        """
        Convert midi pitches in frequency
        
        :param A4: A4 tuning in frequence
        :type A4: float
        :return: list of frequencies
        :rtype: list[float]

        :Example:

        >>> a = _PSet([69, 60, 57, 81])
        >>> print(a.to_freq())
        [440.0, 261.6255653005986, 220.0, 880.0]
        """
        return (A4 * (2 ** ((self.vals - 69) / 12))).tolist()
    
    def to_midi(self, a4: float = 440) -> _PSet:
        """
        Convert frequencies in midi pitches
        :param a4: A4 tuning in frequence
        :type a4: float
        :return: new Self
        :rtype: Self
        
        :Example:

        >>> a = _PSet([440, 265, 220, 880])
        >>> print(a.to_midi())
         _PSet = [69.0, 64.0, 62.0, 81.0]
        """
        return self.__class__((69 + 12 * np.log2(self.vals / a4)).tolist())
    
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

        :Example:
        
        >>> a = [440, 261, 220, 880]
        >>> b = _PSet.from_freq(a)
        >>> print(b)
        _PSet = [69, 60, 57, 81]
        """
        return cls((69 + 12 * np.log2(np.array(freqs) / a4)).tolist())

    def to_range(self, min: int, max: int) -> Self:
        """
        Move a list of notes to a specific range. If possibile without pitch change, otherwhise min if lower, max if higher.

        :param min: min value of range
        :type min: int
        :param max: max value of range
        :type max: int
        :return: New Self
        :rtype: Self

        :Example:

        >>> a = _PSet(ScaleModel.maj, 60)
        >>> b = a.to_range(36, 48)
        >>> print(b)
        _PSet = [36, 38, 40, 41, 43, 45, 47]
        """
        out = []
        for nota in self.values:
            # Se già nel range, lascia invariato
            if min <= nota <= max:
                out.append(nota)
                continue
                
            pitch11 = nota % 12
            octave = min // 12
            candidate = octave * 12 + pitch11

            while candidate < min:
                candidate += 12
            if candidate > max:
                candidate -= 12
                if candidate < min:
                    candidate = min if abs(nota - min) < abs(nota - max) else max
            out.append(candidate)
        return self.__class__(out)

    def micro_quanta(self, tone_div: int) -> Self:
        """
        Quantazie to nearest tone division

        :param tone_div: tone subdivision
        :type tone_div: int
        :return: self
        :rtype: Self

        :Example:

        >>> a = _PSet([60.1, 62.3, 63.7, 64.5, 65.9, 66.2, 67.8])
        >>> b = a.micro_quanta(4)
        >>> print(b)
        _PSet = [60.0, 62.25, 63.75, 64.5, 65.75, 66.25, 67.75]
        """
        self.vals = np.round(self.vals * tone_div) / tone_div
        return self
    
    def scale_quanta(self, scale: ScaleModel | ArrayLike, unique: bool = False) -> Self:
        """Quantize to nearest note of scale
        :param scale: scale model or list of intervals
        :type scale: ScaleModel | ArrayLike
        :param unique: if True, return only one note for each pitch class, default False
        :type unique: bool
        :return: new Self
        :rtype: Self
        
        :Example:
        
        >>> a = _PSet([60, 62, 63, 64, 65, 66, 67])
        >>> b = a.scale_quanta(ScaleModel.maj, True)
        >>> print(b)
        _PSet = [60, 62, 64, 65, 67]
        """
        sc = np.asanyarray(scale['intervals']) if isinstance(scale, dict) else np.asanyarray(scale)
        sc = sc % 12

        pitch11 = self.vals % 12
        diff = np.abs(pitch11[:, None] - sc[None, :])
        circ_diff = np.minimum(diff, 12 - diff)
        candidate = sc[np.argmin(circ_diff, axis=1)]
        octaves = self.vals // 12
        result = octaves * 12 + candidate
        new = self.__class__(result.tolist(), 0)
        if unique:
            new.unique('normal')
        return new    

class Scale(_PSet):

    chords: list[Chord]

    def __init__(self, intervals: ArrayLike, root: Numeric = 0, harmo: ArrayLike = None) -> None:
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

    def n_inversion(self, pos: int) -> Chord:
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
    
    def octaver(self, octaves: ArrayLike) -> Chord:
        """
        Shif by octaves specific pitches of chord

        :param octaves: array of octave
        :type octaves: ArrayLike
        :return: New Chord
        :rtype: Self

        :Example:

        >>> a = Chord([60, 62, 63])
        >>> b = a.octaver([0, 1, -1])
        print(b)
        Chord = [60, 74, 51]
        """
        return self.__class__((self.vals + np.array(octaves) * 12).tolist())

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
    
    def drop(self, pos: int) -> Chord:
        """
        Drop note at specific position by single octave, up or down

        :param pos: position of drop
        :type pos: int
        :return: New Chord
        :rtype: Chord

        :Example:

        >>> a = Chord([0, 1, 2, 3, 4]).drop(3)
        >>> print(a)
        >>> Chord = [0, 1, -10, 3, 4]
        """
        octaves = np.array([0]*len(self))
        octaves[-pos] = -1
        new = self.octaver(octaves)
        return new
    
    @property
    def drop2(self) -> Chord:
        """
        Drop the second highest note

        :return: New Chord
        :rtype: Chord

        :Example:

        >>> a = Chord([0, 4, 7, 10], 60).drop2
        >>> print(a)
        >>> Chord = [60, 64, 55, 70]
        """
        return self.drop(2)
    
    @property
    def drop3(self) -> Chord:
        """
        Drop the third highest note

        :return: New Chord
        :rtype: Chord

        :Example:

        >>> a = Chord([0, 4, 7, 10], 60).drop3
        >>> print(a)
        >>> Chord = [60, 52, 67, 70]
        """
        return self.drop(3)

class Spectra(_PSet):
    
    def __init__(self, freqs: ArrayLike) -> None:
        """
        Rappresentation of a spectra

        :param freqs: list of frequencies
        :type freqs: ArrayLike
        """
        super().__init__(values=freqs, offset=0)

    @classmethod
    def harm_series(cls, fond: float, lenght: int, factor: float = 1) -> Spectra:
        """
        Create harmonic series from fondamental frequency.
        
        :param fond: fondamental frequency
        :type fond: float
        :param lenght: number of partials
        :type lenght: int
        :param factor: factor of partials, default 1 (harmonic series)
        :type factor: float
        :param a4: A4 tuning in frequence
        :type a4: float
        :return: new Spectra
        :rtype: Spectra
        
        :Example:

        >>> a = Spectra.harm_series(55, 8, 1)
        >>> print(a)
        Spectra = [33.0, 45.0, 52.0, 57.0, 61.0, 64.0, 67.0, 69.0]
        """

        pitches = np.arange(1, lenght+1) * factor
        pitches[0] = 1
        pitches *= fond
        return cls(pitches.tolist())
    
    def ring_mod(self, mod: float) -> Spectra:
        """
        Ring modulation of spectra with carrier

        :param carrier: carrier for ring modulation
        :type carrier: _PSet
        :param mod: modulation index
        :type mod: float
        :return: new Spectra
        :rtype: Spectra

        :Example:

        >>> a = Spectra.harm_series(55, 8, 1)
        >>> b = a.ring_mod(Scale.new(ScaleModel.maj, 60), 0.5)
        >>> print(b)
        Spectra = [15.0, 22.5, 26.0, 28.5, 30.5, 32.0, 33.5, 34.5]
        """
        out = []
        for f in enumerate(self.vals):
            out.append(f[1] - mod)
            out.append(f[1] + mod)
        out = np.abs(out, dtype=float).tolist()
        
        return self.__class__(out)
    
    @classmethod
    def to_ring_mod(cls, carrier: Chord | Scale | _PSet, mod: float, a4: float = 440) -> Spectra:
        """
        Ring modulation of a carrier with modulation index
        
        :param carrier: carrier for ring modulation
        :type carrier: Chord | Scale | _PSet
        :param mod: modulation index
        :type mod: float
        :param a4: A4 tuning in frequence
        :type a4: float
        :return: new Spectra
        :rtype: Spectra
        
        :Example:

        >>> a = Chord([0, 4, 7], 60)
        >>> b = Spectra.to_ring_mod(a, 21.234)
        >>> print(b)
        Spectra = [418.61, 481.83, 523.25, 461.77, 440.0, 502.46]
        """
        spettro = Spectra(carrier.to_freq(a4)).ring_mod(mod=mod)
        return spettro