******************************
Data
******************************

.. currentmodule:: musicnpy.data

Introduction
===================
This module provide a collection of models available in the library for different types of musical data. It provides predefined chord patterns that can be used to generate chords based on a root note.

Chords Model
===================

ChordModel is a class for handling chord models in musical data.

.. autoclass:: ChordModel
   :members:
   :undoc-members:
   :show-inheritance:


Scales Model
===================
ScaleModel is a class for handling scale models in musical data. It provides predefined scale patterns that can be used to generate scales based on a root note.
It includes the chords of the scale as well, which are derived from the intervals of the scale.
  
.. autoclass:: ScaleModel
   :members:
   :undoc-members:
   :show-inheritance: