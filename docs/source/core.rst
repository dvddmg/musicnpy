====================
Core
====================
--------------------

.. currentmodule:: musicnpy.core


Introduction
===================
This module provides the base class :class:`_Set` for manipulating musical numeric sequences, integrating vectorial operations through NumPy.
It serves as the foundation for more specialized classes in the library, enabling efficient and readable data transformation pipelines for musical data.

|

_Set Class
===================

The ``core`` module provides the base class :class:`_Set` for manipulating musical numeric sequences, integrating vectorial operations through NumPy.
The class accepts NumPy arrays, Python lists, or other _Set objects as input.
Operations can be chained to create efficient and readable data transformation pipelines for musical data.
The class supports arithmetic operations, mathematical transformations, structural manipulations, and logical filters, all optimized for music processing.
Most of these operations return new ``_Set`` objects, allowing the original objects to remain unchanged and facilitating work with complex musical sequences.
In some cases, as documented, operations can be performed in-place to improve performance.

.. code-block:: python
   
   from musicnpy import _Set

   s = _Set([0, 2, 4, 5, 7, 9, 11], 60)

   print(s.values)

|

Lifecycle & Setup
--------------------
Initialization and basic methods for resetting, copying, and representing the _Set object.

.. automethod:: _Set.__init__
.. autoattribute:: _Set.reset
.. autoattribute:: _Set.copy
.. automethod:: _Set.__repr__

|

Getters & Properties
-----------------------
These properties and methods allow access to various attributes of the _Set object, such as its values, original input, deltas between values, median, odd and even indexed values, and more.

.. autoattribute:: _Set.values
.. autoattribute:: _Set.original
.. autoattribute:: _Set.deltas
.. autoattribute:: _Set.median
.. autoattribute:: _Set.odd
.. autoattribute:: _Set.even
.. automethod:: _Set.__len__
.. automethod:: _Set.getitems
.. automethod:: _Set.getids
.. automethod:: _Set.__getitem__
.. automethod:: _Set.__setitem__

|

Arithmetic Operations
-------------------------

All arithmetic operations support scalars (single numbers) or sequences (lists, arrays or other _Set).

Operations can be performed between _Set of different lengths; in this case, internally the sets are aligned to the length of the larger one.
Additional elements are filled with zeros for addition and subtraction, and with one for multiplication, division, power and modulo.

.. automethod:: _Set.__add__
.. automethod:: _Set.__iadd__
.. automethod:: _Set.__radd__
.. automethod:: _Set.__sub__
.. automethod:: _Set.__isub__
.. automethod:: _Set.__rsub__
.. automethod:: _Set.__mul__
.. automethod:: _Set.__imul__
.. automethod:: _Set.__rmul__
.. automethod:: _Set.__truediv__
.. automethod:: _Set.__itruediv__
.. automethod:: _Set.__rtruediv__
.. automethod:: _Set.__floordiv__
.. automethod:: _Set.__ifloordiv__
.. automethod:: _Set.__rfloordiv__
.. automethod:: _Set.__pow__
.. automethod:: _Set.__ipow__
.. automethod:: _Set.__rpow__
.. automethod:: _Set.__mod__
.. automethod:: _Set.__imod__
.. automethod:: _Set.__rmod__
.. automethod:: _Set.__abs__
.. automethod:: _Set._abs
.. automethod:: _Set.__neg__
.. automethod:: _Set._neg

|

Mathematical Transformations
-----------------------------
These methods apply various mathematical transformations to the sequence, such as transposition, shifting, scaling, limiting values, inverting, rounding, and more.

.. automethod:: _Set.shift
.. automethod:: _Set.scaled
.. automethod:: _Set.limit
.. automethod:: _Set.invert
.. automethod:: _Set.__invert__
.. automethod:: _Set.round
.. automethod:: _Set.ceil
.. automethod:: _Set.floor

|

Structural Manipulation
----------------------------
These methods allow for structural changes to the sequence, such as splitting, sorting, reversing, rotating, inserting, removing elements, and more.

.. automethod:: _Set.split
.. automethod:: _Set.interleave
.. automethod:: _Set.sort
.. automethod:: _Set.reverse
.. automethod:: _Set.rotate
.. automethod:: _Set.insert
.. automethod:: _Set.remove
.. automethod:: _Set.unique
.. automethod:: _Set.append
.. automethod:: _Set.pad
.. automethod:: _Set.repeat
.. automethod:: _Set.__lshift__
.. automethod:: _Set.__ilshift__
.. automethod:: _Set.concat
.. automethod:: _Set.__or__
.. automethod:: _Set.__ior__

|

Logic, Filters and Sequences
----------------------------
These methods allow for logical operations, filtering based on conditions, and retrieving sequences of values.

.. automethod:: _Set.filter
.. automethod:: _Set.getseq
.. automethod:: _Set.__iter__

|

Internal Methods
-----------------
These methods are used internally by the class and are not typically called directly.

.. automethod:: _Set._align
.. automethod:: _Set._binary_op