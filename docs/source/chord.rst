******************************
Chord
******************************
--------------------

.. currentmodule:: musicnpy.pitch


Introduction
===================
This module provides the :class:`Chord` class for manipulating musical chords.
A chord is a collection of pitches (notes) that are played together, defined by a list of intervals relative to a root note.
The Chord class extends :class:`_PSet` and inherits all vectorial operations and transformations from the core :class:`_Set` class.
This allows chords to be manipulated using arithmetic operations, mathematical transformations, and structural manipulations,
facilitating complex harmonic transformations and chord progressions.

|

Chord Class
===================

The :class:`Chord` class represents a musical chord as a collection of pitches.
It extends the :class:`_PSet` class, which in turn extends :class:`_Set`.
Chords are defined by specifying intervals (relative to a root note) or by using predefined chord models from the :class:`ChordModel` database.
Most operations return new Chord objects, allowing the original chord to remain unchanged.

.. code-block:: python
   
   from musicnpy import Chord, ChordModel

   # Create a chord by specifying intervals and root note
   c = Chord([0, 4, 7], 60)
   print(c.pitches)  # [60, 64, 67]

   # Create a chord from a predefined model
   maj = Chord.new(ChordModel.maj, 60)
   print(maj.pitches)  # [60, 64, 67]

   # Perform operations
   inverted = c.first_inv  # First inversion
   transposed = c + 12  # Transpose up an octave
   scaled = c * 1.5  # Scale dynamic envelope

|

Initialization & Creation
---------------------------
Methods for creating and initializing Chord objects from intervals, models, or other data sources.

.. automethod:: Chord.__init__
.. automethod:: Chord.new

|

Pitch Properties
------------------
Properties for accessing pitch information in various formats.

.. autoattribute:: Chord.pitches
.. autoattribute:: Chord.intervals
.. autoattribute:: Chord.root
.. automethod:: Chord.to_freq
.. automethod:: Chord.from_freq

|

Inversions
-----------
Methods for generating different voicings of the chord through inversions.
Inversions move the root note or other lower notes up by one or more octaves.

.. automethod:: Chord.n_inversion
.. autoattribute:: Chord.first_inv
.. autoattribute:: Chord.second_inv

|

Arithmetic Operations
------------------------

All arithmetic operations from the base :class:`_Set` class are available on Chord objects.
Operations can be performed between Chords of different sizes or between a Chord and scalar values.

Supported operations include:

.. automethod:: Chord.__add__
.. automethod:: Chord.__iadd__
.. automethod:: Chord.__radd__
.. automethod:: Chord.__sub__
.. automethod:: Chord.__isub__
.. automethod:: Chord.__rsub__
.. automethod:: Chord.__mul__
.. automethod:: Chord.__imul__
.. automethod:: Chord.__rmul__
.. automethod:: Chord.__truediv__
.. automethod:: Chord.__itruediv__
.. automethod:: Chord.__rtruediv__
.. automethod:: Chord.__floordiv__
.. automethod:: Chord.__ifloordiv__
.. automethod:: Chord.__rfloordiv__
.. automethod:: Chord.__pow__
.. automethod:: Chord.__ipow__
.. automethod:: Chord.__rpow__
.. automethod:: Chord.__mod__
.. automethod:: Chord.__imod__
.. automethod:: Chord.__rmod__
.. automethod:: Chord.__abs__
.. automethod:: Chord.__neg__

|

Mathematical Transformations
-----------------------------
Methods for applying mathematical transformations to chord pitches.

.. automethod:: Chord.shift
.. automethod:: Chord.scaled
.. automethod:: Chord.limit
.. automethod:: Chord.invert
.. automethod:: Chord.__invert__
.. automethod:: Chord.round
.. automethod:: Chord.ceil
.. automethod:: Chord.floor
.. automethod:: Chord.interpolation
.. automethod:: Chord.normalize

|

Structural Manipulation
----------------------------
Methods for modifying the structure and ordering of chord pitches.

.. automethod:: Chord.split
.. automethod:: Chord.interleave
.. automethod:: Chord.sort
.. automethod:: Chord.reverse
.. automethod:: Chord.rotate
.. automethod:: Chord.insert
.. automethod:: Chord.remove
.. automethod:: Chord.unique
.. automethod:: Chord.append
.. automethod:: Chord.repeat
.. automethod:: Chord.__lshift__
.. automethod:: Chord.concat
.. automethod:: Chord.__or__

|

Logic, Filters and Sequences
-----------------------------
Methods for filtering and logical operations on chords.

.. automethod:: Chord.filter
.. automethod:: Chord.getseq
.. automethod:: Chord.__iter__

|

Generators
-----------
Class methods for generating Chord objects with random or specific values.

.. automethod:: Chord.rand_int
.. automethod:: Chord.rand_flt
.. automethod:: Chord.n_time

|

Getters & Utilities
---------------------
Methods and properties for accessing specific elements and information about the chord.

.. autoattribute:: Chord.values
.. autoattribute:: Chord.original
.. autoattribute:: Chord.deltas
.. autoattribute:: Chord.mean
.. autoattribute:: Chord.odd
.. autoattribute:: Chord.even
.. autoattribute:: Chord.profile
.. automethod:: Chord.__len__
.. automethod:: Chord.getitems
.. automethod:: Chord.getids
.. automethod:: Chord.__getitem__
.. automethod:: Chord.__setitem__
.. automethod:: Chord.copy
.. automethod:: Chord.__repr__

|

Internal Methods
-----------------
These methods are used internally by the class and are not typically called directly.

.. automethod:: Chord._align
.. automethod:: Chord._binary_op
.. automethod:: Chord._abs
.. automethod:: Chord._neg

|
