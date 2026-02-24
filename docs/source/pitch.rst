******************************
Pitch
******************************

.. currentmodule:: musicnpy.pitch

Introduction
===================
This module provides classes and methods for handling musical pitch data.
It includes the :class:`_PSet` private class, which extends the core :class:`_Set` class to specifically manage pitch-related operations.
The module also provides the :class:`Chord` and :class:`Scale` classes for handling chords and scales, respectively.

_PSet Class
===================

The :class:`_PSet` class extends the core :class:`_Set` class to add pitch-specific functionality.
It adds properties and methods for handling MIDI pitches, intervals, root notes, and frequency conversions.
This class serves as the base for more specialized pitch classes like :class:`Chord` and :class:`Scale`.

.. automethod:: _PSet.__init__
   :no-index:
.. autoattribute:: _PSet.pitches
.. autoattribute:: _PSet.intervals
.. autoattribute:: _PSet.root
.. automethod:: _PSet.to_freq
.. automethod:: _PSet.to_midi
.. automethod:: _PSet.from_freq
.. automethod:: _PSet.to_range
.. automethod:: _PSet.micro_quanta
.. automethod:: _PSet.scale_quanta

Chord Class
===================

The :class:`Chord` class represents a musical chord as a collection of pitches.
It extends :class:`_PSet` and provides methods for creating chords from models, inverting chords, and manipulating chord notes.
Chords are defined by a list of intervals relative to a root note, and they inherit all operations from the :class:`_Set` class.

.. code-block:: python
   
   from musicnpy import Chord, ChordModel

   # Create a chord by specifying intervals and root
   c = Chord([0, 4, 7], 60)
   print(c.pitches)  # [60, 64, 67]

   # Create a chord from a model
   maj = Chord.new(ChordModel.maj, 60)
   print(maj)

.. automethod:: Chord.__init__
.. automethod:: Chord.new
.. automethod:: Chord.n_inversion
.. autoattribute:: Chord.first_inv
.. autoattribute:: Chord.second_inv
.. automethod:: Chord.drop
.. autoattribute:: Chord.drop2
.. autoattribute:: Chord.drop3
.. automethod:: Chord.octaver

Scale Class
===================

The :class:`Scale` class represents a musical scale as an ordered collection of pitches.
It extends :class:`_PSet` and adds harmonic and diatonic degree functionality.
Scales can be created from interval patterns or from scale models in the database.

.. code-block:: python
   
   from musicnpy import Scale, ScaleModel

   # Create a scale by specifying intervals and root
   s = Scale([0, 2, 4, 5, 7, 9, 11], 60)
   print(s.pitches)  # [60, 62, 64, 65, 67, 69, 71]

   # Create a scale from a model
   maj = Scale.new(ScaleModel.maj, 60)
   print(maj)

.. automethod:: Scale.__init__
.. automethod:: Scale.new
.. autoattribute:: Scale.diatonic
.. autoattribute:: Scale.harmonize

Spectra Class
===================
``Spectra`` allow to create a collection of frequencies, that can be used to create a chord or a scale.
It also provied some class method for create spectra series.

.. code-block:: python

   from musicnpy import Spectra

   # Create a spectra by specifying frequencies
   s = Spectra([440, 880, 1320])
   print(s.frequencies)  # [440, 880, 1320]
   
.. automethod:: Spectra.__init__
.. automethod:: Spectra.harm_series
.. automethod:: Spectra.ring_mod
.. automethod:: Spectra.to_ring_mod