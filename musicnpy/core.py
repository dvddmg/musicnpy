from __future__ import annotations
"""
musicnpy.core 
il core alla basa della libreria musicnpy.
"""

import numpy as np
import numbers, operator
from typing import Self, TypeAlias, Callable, Any, Literal
from collections.abc import Sequence, Iterator

Numeric = numbers.Real
ArrayLike: TypeAlias = '_Set | Sequence[Numeric]'
Index = int | slice | Sequence[int] | np.ndarray

class _Set:

    def __init__(self, list: list[Numeric], offset: Numeric = 0) -> _Set:
        
        """
        Initialize a _Set with a list of numeric values.

        Creates a new _Set instance containing numeric values with an optional
        offset applied to all elements.

        :param list: List of numeric values to initialize the set with.
        :type list: list[Numeric]
        :param offset: Value to add to all elements. Defaults to 0.
        :type offset: Numeric
        :return: A new _Set instance.
        :rtype: _Set

        :Example:

        >>> s = _Set([1, 2, 3], offset=10)
        >>> s.values
        [11.0, 12.0, 13.0]
        """

        self.offset: Numeric = offset
        self.set: np.ndarray = np.array(list) + self.offset
        self.vals: np.ndarray = self.set.copy()

    @property
    def deltas(self) -> list[Numeric]:

        """
        Compute the differences between consecutive elements.

        :return: List of differences between each pair of consecutive elements.
        :rtype: list[Numeric]

        :Example:

        >>> s = _Set([1, 3, 6, 10])
        >>> s.deltas
        [2.0, 3.0, 4.0]
        """

        return np.diff(self.vals).tolist()
    
    @property
    def odd(self) -> list[Numeric]:
        
        """
        Retrieve all odd-valued elements from the set.

        :return: List containing only elements with odd values.
        :rtype: list[Numeric]

        :Example:

        >>> s = _Set([1, 2, 3, 4, 5])
        >>> s.odd
        [1.0, 3.0, 5.0]
        """

        return self.vals[self.vals % 2 == 1].tolist()
    
    @property
    def even(self) -> list[Numeric]:
        
        """
        Retrieve all even-valued elements from the set.

        :return: List containing only elements with even values.
        :rtype: list[Numeric]

        :Example:

        >>> s = _Set([1, 2, 3, 4, 5])
        >>> s.even
        [2.0, 4.0]
        """

        return self.vals[self.vals % 2 == 0].tolist()

    @property
    def values(self) -> list[Numeric]:
        
        """
        Retrieve the current values as a list.

        Returns the working copy of values, which may have been modified
        since initialization.

        :return: List of current values in the set.
        :rtype: list[Numeric]

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> s.values
        [1.0, 2.0, 3.0]
        """

        return self.vals.tolist()

    @property
    def original(self) -> list[Numeric]:
        
        """
        Retrieve the original unmodified values.

        Returns the values as they were at initialization (with offset applied),
        regardless of any subsequent modifications.

        :return: List of original values.
        :rtype: list[Numeric]

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> s += 10
        >>> s.original
        [1.0, 2.0, 3.0]
        """

        return self.set.tolist()

    @property
    def reset(self) -> Self:

        """
        Reset values to their original state.

        Restores the working values to match the original values stored
        at initialization.

        :return: This set instance with values reset.
        :rtype: Self

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> s += 10
        >>> s.reset.values
        [1.0, 2.0, 3.0]
        """

        self.vals = self.set.copy()
        return self

    @property
    def median(self) -> Numeric:
        
        """
        Compute the median value of the set.

        For sets with an even number of elements, returns the average
        of the two middle values.

        :return: The median value.
        :rtype: Numeric

        :Example:

        >>> s = _Set([1, 3, 5, 7, 9])
        >>> s.median
        5.0
        """

        return np.median(self.vals)

    @property
    def copy(self) -> _Set:

        """
        Create a deep copy of this set.

        Returns a new _Set instance with copies of all internal arrays,
        ensuring modifications to the copy do not affect the original.

        :return: A new independent copy of this set.
        :rtype: _Set

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> s_copy = s.copy
        >>> s_copy += 10
        >>> s.values
        [1.0, 2.0, 3.0]
        """

        new = self.__class__.__new__(self.__class__)
        new.offset = self.offset
        new.set = self.set.copy()
        new.vals = self.vals.copy()
        return new

    def __len__(self) -> int:
        
        """
        Return the number of elements in the set.

        :return: Number of elements.
        :rtype: int

        :Example:

        >>> s = _Set([1, 2, 3, 4, 5])
        >>> len(s)
        5
        """

        return len(self.vals)

    def __iter__(self) -> Iterator[Numeric]:
        
        """
        Return an iterator over the set's elements.

        :return: Iterator yielding each element in order.
        :rtype: Iterator[Numeric]

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> list(s)
        [1.0, 2.0, 3.0]
        """

        return iter(self.vals)

    def _align(self, other: ArrayLike | Numeric, fill: Numeric) -> tuple[np.ndarray, np.ndarray]:

        """
        Align two arrays to the same length by padding the shorter one.

        :param other: The array or set to align with.
        :type other: ArrayLike | Numeric
        :param fill: Value used to pad the shorter array.
        :type fill: Numeric
        :return: Tuple of two aligned numpy arrays of equal length.
        :rtype: tuple[np.ndarray, np.ndarray]

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> a, b = s._align([4, 5], fill=0)
        >>> b.tolist()
        [4.0, 5.0, 0.0]
        """

        a = self.vals
        b = other.vals if isinstance(other, _Set) else np.array(other)
        if len(b) < len(a):
            b = self.pad(b.tolist(), len(a) - len(b), fill)
        elif len(b) > len(a):
            a = self.pad(a.tolist(), len(b) - len(a), fill)
        return np.array(a), np.array(b)

    def _binary_op(self, other: ArrayLike | Numeric, op: Callable[[Any, Any], np.ndarray], fill: Numeric = 0, reversed: bool = False) -> _Set:

        """
        Perform a binary operation between this set and another operand.

        :param other: The right-hand operand (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :param op: The binary operator function to apply.
        :type op: Callable[[Any, Any], np.ndarray]
        :param fill: Value used to pad shorter arrays during alignment. Defaults to 0.
        :type fill: Numeric
        :param reversed: If True, swap operand order. Defaults to False.
        :type reversed: bool
        :return: Result of the operation as a numpy array.
        :rtype: np.ndarray
        :raises TypeError: If the operand type is not supported.

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> result = s._binary_op(10, operator.add)
        >>> result.tolist()
        [11.0, 12.0, 13.0]
        """

        with np.errstate(divide="ignore", invalid="ignore"):
            if isinstance(other, (_Set, list)):
                a, b = self._align(other, fill)
                lhs, rhs = (b, a) if reversed else (a, b)
                result = op(lhs, rhs)
            elif isinstance(other, numbers.Real):
                lhs, rhs = (other, self.vals) if reversed else (self.vals, other)
                result = op(lhs, rhs)
            else:
                raise TypeError("Not implemented")
            
            return result

    def __add__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Add values element-wise using the ``+`` operator.

        :param other: Values to add (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: A new set with the sum of values.
        :rtype: _Set

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> (s + 10).values
        [11.0, 12.0, 13.0]
        """

        return _Set(self._binary_op(other, operator.add, fill=0))

    def __radd__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Add values with reversed operand order using the ``+`` operator.

        :param other: Values to add (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: A new set with the sum of values.
        :rtype: _Set

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> (10 + s).values
        [11.0, 12.0, 13.0]
        """

        return _Set(self._binary_op(other, operator.add, fill=0, reversed=True))

    def __iadd__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Add values in-place using the ``+=`` operator.

        :param other: Values to add (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: This set with updated values.
        :rtype: Self

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> s += 5
        >>> s.values
        [6.0, 7.0, 8.0]
        """

        self.vals = self._binary_op(other, operator.add, fill=0)
        return self

    def __sub__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Subtract values element-wise using the ``-`` operator.

        :param other: Values to subtract (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: A new set with the difference of values.
        :rtype: _Set

        :Example:

        >>> s = _Set([10, 20, 30])
        >>> (s - 5).values
        [5.0, 15.0, 25.0]
        """

        return _Set(self._binary_op(other, operator.sub, fill=0))

    def __rsub__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Subtract with reversed operand order using the ``-`` operator.

        :param other: Value to subtract from (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: A new set with the difference of values.
        :rtype: _Set

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> (10 - s).values
        [9.0, 8.0, 7.0]
        """

        return _Set(self._binary_op(other, operator.sub, fill=0, reversed=True))

    def __isub__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Subtract values in-place using the ``-=`` operator.

        :param other: Values to subtract (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: This set with updated values.
        :rtype: Self

        :Example:

        >>> s = _Set([10, 20, 30])
        >>> s -= 5
        >>> s.values
        [5.0, 15.0, 25.0]
        """

        self.vals = self._binary_op(other, operator.sub, fill=0)
        return self

    def __mul__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Multiply values element-wise using the ``*`` operator.

        :param other: Values to multiply by (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: A new set with the product of values.
        :rtype: _Set

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> (s * 10).values
        [10.0, 20.0, 30.0]
        """

        return _Set(self._binary_op(other, operator.mul, fill=1))

    def __rmul__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Multiply with reversed operand order using the ``*`` operator.

        :param other: Values to multiply by (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: A new set with the product of values.
        :rtype: _Set

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> (10 * s).values
        [10.0, 20.0, 30.0]
        """

        return _Set(self._binary_op(other, operator.mul, fill=1, reversed=True))

    def __imul__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Multiply values in-place using the ``*=`` operator.

        :param other: Values to multiply by (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: This set with updated values.
        :rtype: Self

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> s *= 5
        >>> s.values
        [5.0, 10.0, 15.0]
        """

        self.vals = self._binary_op(other, operator.mul, fill=1)
        return self

    def __truediv__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Divide values element-wise using the ``/`` operator.

        :param other: Values to divide by (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: A new set with the quotient of values.
        :rtype: _Set

        :Example:

        >>> s = _Set([10, 20, 30])
        >>> (s / 2).values
        [5.0, 10.0, 15.0]
        """

        return _Set(self._binary_op(other, operator.truediv, fill=1))

    def __rtruediv__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Divide with reversed operand order using the ``/`` operator.

        :param other: Value to be divided (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: A new set with the quotient of values.
        :rtype: _Set

        :Example:

        >>> s = _Set([2, 4, 5])
        >>> (20 / s).values
        [10.0, 5.0, 4.0]
        """

        return _Set(self._binary_op(other, operator.truediv, fill=1, reversed=True))

    def __itruediv__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Divide values in-place using the ``/=`` operator.

        :param other: Values to divide by (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: This set with updated values.
        :rtype: Self

        :Example:

        >>> s = _Set([10, 20, 30])
        >>> s /= 2
        >>> s.values
        [5.0, 10.0, 15.0]
        """

        self.vals = self._binary_op(other, operator.truediv, fill=1)
        return self
    
    def __floordiv__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Perform floor division element-wise using the ``//`` operator.

        :param other: Values to divide by (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: A new set with the floor-divided values.
        :rtype: _Set

        :Example:

        >>> s = _Set([10, 20, 30])
        >>> (s // 3).values
        [3.0, 6.0, 10.0]
        """

        return _Set(self._binary_op(other, operator.floordiv, fill=1))
    
    def __rfloordiv__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Perform floor division with reversed operand order using the ``//`` operator.

        :param other: Value to be divided (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: A new set with the floor-divided values.
        :rtype: _Set

        :Example:

        >>> s = _Set([3, 4, 5])
        >>> (20 // s).values
        [6.0, 5.0, 4.0]
        """

        return _Set(self._binary_op(other, operator.floordiv, fill=1, reversed=True))
    
    def __ifloordiv__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Perform floor division in-place using the ``//=`` operator.

        :param other: Values to divide by (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: This set with updated values.
        :rtype: Self

        :Example:

        >>> s = _Set([10, 20, 30])
        >>> s //= 3
        >>> s.values
        [3.0, 6.0, 10.0]
        """

        self.vals = self._binary_op(other, operator.floordiv, fill=1)
        return self

    def __pow__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Raise values to a power element-wise using the ``**`` operator.

        :param other: Exponent values (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: A new set with exponentiated values.
        :rtype: _Set

        :Example:

        >>> s = _Set([2, 3, 4])
        >>> (s ** 2).values
        [4.0, 9.0, 16.0]
        """

        return _Set(self._binary_op(other, operator.pow, fill=1))

    def __rpow__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Raise to a power with reversed operand order using the ``**`` operator.

        :param other: Base value (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: A new set with exponentiated values.
        :rtype: _Set

        :Example:

        >>> s = _Set([2, 3, 4])
        >>> (2 ** s).values
        [4.0, 8.0, 16.0]
        """

        return _Set(self._binary_op(other, operator.pow, fill=1, reversed=True))

    def __ipow__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Raise values to a power in-place using the ``**=`` operator.

        :param other: Exponent values (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: This set with updated values.
        :rtype: Self

        :Example:

        >>> s = _Set([2, 3, 4])
        >>> s **= 2
        >>> s.values
        [4.0, 9.0, 16.0]
        """
        
        self.vals = self._binary_op(other, operator.pow, fill=1)
        return self
    
    def __mod__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Compute modulo element-wise using the ``%`` operator.

        :param other: Divisor values (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: A new set with remainder values.
        :rtype: _Set

        :Example:

        >>> s = _Set([10, 15, 20])
        >>> (s % 3).values
        [1.0, 0.0, 2.0]
        """
        
        return _Set(self._binary_op(other, operator.mod, fill=1))

    def __rmod__(self, other: ArrayLike | Numeric) -> _Set:

        """
        Compute modulo with reversed operand order using the ``%`` operator.

        :param other: Dividend value (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: A new set with remainder values.
        :rtype: _Set

        :Example:

        >>> s = _Set([3, 4, 6])
        >>> (20 % s).values
        [2.0, 0.0, 2.0]
        """

        return _Set(self._binary_op(other, operator.mod, fill=1, reversed=True))

    def __imod__(self, other: ArrayLike | Numeric) -> _Set:
        
        """
        Compute modulo in-place using the ``%=`` operator.

        :param other: Divisor values (set, sequence, or scalar).
        :type other: ArrayLike | Numeric
        :return: This set with updated values.
        :rtype: Self

        :Example:

        >>> s = _Set([10, 15, 20])
        >>> s %= 3
        >>> s.values
        [1.0, 0.0, 2.0]
        """

        self.vals = self._binary_op(other, operator.mod, fill=1)
        return self

    def __repr__(self) -> str:
        
        """
        Return a string representation of the set.

        :return: String in the format ``ClassName = [values]``.
        :rtype: str

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> repr(s)
        '_Set = [1.0, 2.0, 3.0]'
        """

        return f'{self.__class__.__name__} = {self.values}'

    def __getitem__(self, key: Index) -> Numeric:
        
        """
        Retrieve element(s) by index using bracket notation.

        :param key: Index, slice, or sequence of indices.
        :type key: Index
        :return: The element or list of elements at the specified position(s).
        :rtype: Numeric | list[Numeric]
        :raises TypeError: If key type is not supported.

        :Example:

        >>> s = _Set([10, 20, 30, 40, 50])
        >>> s[0]
        10.0
        """

        if isinstance(key, slice) or isinstance(key, int):
            return self.vals[key].tolist()
        else:
            raise TypeError('Invalid index type')

    def __setitem__(self, key: Index, value: ArrayLike | Numeric) -> _Set:
        
        """
        Set element(s) by index using bracket notation.

        :param key: Index or slice to modify.
        :type key: Index
        :param value: New value(s) to assign.
        :type value: ArrayLike | Numeric
        :return: This set with updated values.
        :rtype: Self
        :raises TypeError: If key type is not supported.

        :Example:

        >>> s = _Set([1, 2, 3, 4, 5])
        >>> s[0] = 10
        >>> s.values
        [10.0, 2.0, 3.0, 4.0, 5.0]
        """

        if isinstance(key, slice) or isinstance(key, int):
            self.vals[key] = value
            return self
        else:
            raise TypeError('Invalid index type')

    def __abs__(self) -> _Set:
        
        """
        Compute absolute values using the built-in ``abs()`` function.

        :return: A new set with absolute values.
        :rtype: _Set

        :Example:

        >>> s = _Set([-1, -2, 3, -4])
        >>> abs(s).values
        [1.0, 2.0, 3.0, 4.0]
        """

        return type(self)(np.abs(self.values))
    
    def _abs(self) -> Self:
        
        """
        Compute absolute values in-place.

        :return: This set with absolute values applied.
        :rtype: Self

        :Example:

        >>> s = _Set([-1, -2, 3, -4])
        >>> s._abs().values
        [1.0, 2.0, 3.0, 4.0]
        """
        
        self.vals = np.abs(self.vals)
        return self
    
    def __neg__(self) -> _Set:
        
        """
        Negate values using the unary ``-`` operator.

        :return: A new set with negated values.
        :rtype: _Set

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> (-s).values
        [-1.0, -2.0, -3.0]
        """
        
        return type(self)(-self.vals)

    def _neg(self) -> _Set:
        
        """
        Negate values in-place.

        :return: This set with negated values.
        :rtype: Self

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> s._neg().values
        [-1.0, -2.0, -3.0]
        """
        
        self.vals *= -1
        return self
    
    def shift(self, other: Numeric) -> _Set:
        
        """
        Shift all values by adding a constant offset.

        Updates both the values and the offset attribute.

        :param other: The amount to shift by.
        :type other: Numeric
        :return: This set with shifted values.
        :rtype: Self

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> s.shift(10).values
        [11.0, 12.0, 13.0]
        """

        self.offset = other
        return self.__iadd__(other)
    
    def invert(self, pivot: Numeric = None) -> _Set:
        
        """
        Invert values around a pivot point.

        If no pivot is provided, uses the midpoint between the minimum
        and maximum values.

        :param pivot: The pivot point for inversion. Defaults to None (midpoint).
        :type pivot: Numeric
        :return: A new set with inverted values.
        :rtype: _Set

        :Example:

        >>> s = _Set([1, 2, 3, 4, 5])
        >>> s.invert().values
        [5.0, 4.0, 3.0, 2.0, 1.0]
        """

        if pivot == None:
            return type(self)((self.vals.min() + self.vals.max() - self.vals).tolist())
        return type(self)((2 * pivot - self.vals).tolist())
    
    def __invert__(self) -> _Set:
        
        """
        Invert values in-place using the ``~`` operator.

        Inverts values around their midpoint (average of min and max).

        :return: This set with inverted values.
        :rtype: Self

        :Example:

        >>> s = _Set([1, 2, 3, 4, 5])
        >>> (~s).values
        [5.0, 4.0, 3.0, 2.0, 1.0]
        """

        self.vals = self.vals.min() + self.vals.max() - self.vals
        return self

    def scaled(self, min: Numeric = 0, max: Numeric = 1) -> _Set:
        
        """
        Scale values to a specified range.

        Linearly maps all values to fit within the new range [min, max].

        :param min: The minimum of the target range. Defaults to 0.
        :type min: Numeric
        :param max: The maximum of the target range. Defaults to 1.
        :type max: Numeric
        :return: This set with scaled values.
        :rtype: Self

        :Example:

        >>> s = _Set([0, 50, 100])
        >>> s.scaled(0, 10).values
        [0.0, 5.0, 10.0]
        """

        v_min = self.vals.min()
        v_max = self.vals.max()

        self.vals = (min + (self.vals - v_min) * (max - min) / (v_max - v_min))
        return self
    
    def limit(self, min: Numeric = 0, max: Numeric = 1) -> _Set:
        
        """
        Clip values to a specified range.

        Values below ``min`` become ``min``; values above ``max`` become ``max``.

        :param min: The minimum allowed value. Defaults to 0.
        :type min: Numeric
        :param max: The maximum allowed value. Defaults to 1.
        :type max: Numeric
        :return: This set with clipped values.
        :rtype: Self

        :Example:

        >>> s = _Set([1, 5, 10, 15, 20])
        >>> s.limit(5, 15).values
        [5.0, 5.0, 10.0, 15.0, 15.0]
        """

        self.vals.clip(min=min, max=max, out=self.vals)
        return self
    
    def __lshift__(self, n: int = 0) -> _Set:
        
        """
        Repeat the set n times using the ``<<`` operator.

        :param n: Number of repetitions.
        :type n: int
        :return: A new set with repeated elements.
        :rtype: _Set
        :raises ValueError: If n is negative.

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> (s << 2).values
        [1.0, 2.0, 3.0, 1.0, 2.0, 3.0]
        """

        if not isinstance(n, int):
            return NotImplemented
        if n < 0:
            raise ValueError("Repetition count must be non-negative")
        
        new = type(self)(np.tile(self.values, n))
        return new 

    def __ilshift__(self, n: int = 0) -> _Set:
        
        """
        Repeat the set n times in-place using the ``<<=`` operator.

        :param n: Number of repetitions.
        :type n: int
        :return: This set with repeated elements.
        :rtype: Self
        :raises ValueError: If n is negative.
        :raises TypeError: If n is not an integer.

        :Example:

        >>> s = _Set([1, 2])
        >>> s <<= 2
        >>> s.values
        [1.0, 2.0, 1.0, 2.0]
        """

        if not isinstance(n, int):
            raise TypeError("Operand must be an int")
        if n < 0:
            raise ValueError("Repetition count must be non-negative")
        
        self.vals = np.tile(self.vals, n)
        return self

    def __or__(self, other: ArrayLike | Numeric = 0) -> _Set:
        
        """
        Concatenate with another sequence using the ``|`` operator.

        :param other: Sequence or value to concatenate.
        :type other: ArrayLike | Numeric
        :return: A new set with concatenated elements.
        :rtype: _Set

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> (s | [4, 5]).values
        [1.0, 2.0, 3.0, 4.0, 5.0]
        """

        if isinstance(other, Sequence) or isinstance(other, list):
            return type(self)(np.concatenate((self.vals, other)).tolist())
        elif isinstance(other, _Set):
            return type(self)(np.concatenate((self.vals, other.vals)).tolist())
        else:
            return type(self)(np.concatenate((self.vals, np.array([other]))).tolist())
        
    def __ior__(self, other: ArrayLike | Numeric = 0) -> _Set:
        
        """
        Concatenate in-place using the ``|=`` operator.

        :param other: Sequence or value to concatenate.
        :type other: ArrayLike | Numeric
        :return: This set with concatenated elements.
        :rtype: Self

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> s |= [4, 5]
        >>> s.values
        [1.0, 2.0, 3.0, 4.0, 5.0]
        """

        if isinstance(other, Sequence) or isinstance(other, list):
            self.vals = np.concatenate((self.vals, other))
        elif isinstance(other, _Set):
            self.vals = np.concatenate((self.vals, other.vals))
        else:
            self.vals = np.concatenate((self.vals, np.array([other])))
        return self

    def repeat(self, n: int = 0) -> _Set:
        
        """
        Repeat the set n times in-place.

        :param n: Number of repetitions.
        :type n: int
        :return: This set with repeated elements.
        :rtype: Self
        :raises ValueError: If n is negative.

        :Example:

        >>> s = _Set([1, 2])
        >>> s.repeat(3).values
        [1.0, 2.0, 1.0, 2.0, 1.0, 2.0]
        """

        return self.__ilshift__(n)

    def concat(self, other: ArrayLike | Numeric = 0) -> _Set:
        
        """
        Concatenate this set with another sequence or value in-place.

        :param other: Sequence or value to append.
        :type other: ArrayLike | Numeric
        :return: This set with concatenated elements.
        :rtype: Self

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> s.concat([4, 5]).values
        [1.0, 2.0, 3.0, 4.0, 5.0]
        """

        return self.__ior__(other)

    def rotate(self, n: int = 0) -> _Set:
        
        """
        Rotate elements by n positions.

        Positive values rotate right; negative values rotate left.
        Elements that overflow wrap around.

        :param n: Number of positions to rotate.
        :type n: int
        :return: This set with rotated elements.
        :rtype: Self

        :Example:

        >>> s = _Set([1, 2, 3, 4, 5])
        >>> s.rotate(2).values
        [4.0, 5.0, 1.0, 2.0, 3.0]
        """
        
        self.vals = np.roll(self.vals, n)
        return self

    def reverse(self) -> _Set:
        
        """
        Reverse the order of elements in-place.

        :return: This set with elements in reversed order.
        :rtype: Self

        :Example:

        >>> s = _Set([1, 2, 3, 4, 5])
        >>> s.reverse().values
        [5.0, 4.0, 3.0, 2.0, 1.0]
        """

        self.vals = self.vals[::-1]
        return self

    def insert(self, pos: int = 0, other: ArrayLike | Numeric = 0) -> _Set:
        
        """
        Insert element(s) at a specific position.

        :param pos: Index position for insertion. Defaults to 0.
        :type pos: int
        :param other: Element(s) to insert.
        :type other: ArrayLike | Numeric
        :return: This set with inserted elements.
        :rtype: Self

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> s.insert(1, 10).values
        [1.0, 10.0, 2.0, 3.0]
        """
        
        self.vals = np.insert(self.vals, pos, other)
        return self
    
    def remove(self, idx: int | ArrayLike = None, item: Numeric | ArrayLike = None) -> _Set:
        
        """
        Remove elements by index or by value.

        Provide either ``idx`` or ``item``, not both.

        :param idx: Index or indices of elements to remove. Defaults to None.
        :type idx: int | ArrayLike
        :param item: Value or values of elements to remove. Defaults to None.
        :type item: Numeric | ArrayLike
        :return: This set with elements removed.
        :rtype: Self

        :Example:

        >>> s = _Set([1, 2, 3, 4, 5])
        >>> s.remove(idx=2).values
        [1.0, 2.0, 4.0, 5.0]
        """

        if idx != None and isinstance(idx, (Sequence, _Set, int)):
            self.vals = np.delete(self.vals, idx)
        elif item != None and isinstance(item, (Sequence, _Set, int, float)):
            if isinstance(item, (Sequence, _Set)):
                for i in item:
                    self.vals = np.delete(self.vals, np.where(self.vals == i))
            elif isinstance(item, (int, float)):
                self.vals = np.delete(self.vals, np.where(self.vals == item))
        return self
    
    def unique(self, mode: Literal['normal', 'unique', 'consecutive'] = 'normal') -> _Set:
        
        """
        Remove duplicate elements based on the specified mode.

        :param mode: Deduplication mode. Options are:

            - ``'normal'``: Keep first occurrence of each value.
            - ``'unique'``: Keep only values that appear exactly once.
            - ``'consecutive'``: Remove consecutive duplicates only.

            Defaults to ``'normal'``.
        :type mode: Literal['normal', 'unique', 'consecutive']
        :return: This set with duplicates removed.
        :rtype: Self

        :Example:

        >>> s = _Set([1, 2, 2, 3, 3, 3, 4])
        >>> s.unique('normal').values
        [1.0, 2.0, 3.0, 4.0]
        """

        if mode == 'normal':
            _, idx = np.unique(self.vals, return_index=True)
            self.vals = self.vals[np.sort(idx)]
        elif mode == 'unique':
            vals, idx, counts = np.unique(self.vals, return_counts=True, return_index=True)
            unique_idx = idx[counts==1]
            self.vals = self.vals[np.sort(unique_idx)]
        elif mode == 'consecutive':
            self.vals = self.vals[np.insert(self.vals[1:] != self.vals[:-1], 0, True)]
        return self

    def append(self, other: ArrayLike | Numeric = 0) -> _Set:
        
        """
        Append element(s) to the end of the set.

        :param other: Element(s) to append.
        :type other: ArrayLike | Numeric
        :return: This set with appended elements.
        :rtype: Self

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> s.append(4).values
        [1.0, 2.0, 3.0, 4.0]
        """

        self.vals = np.append(self.vals, other)
        return self

    def pad(self, n_pad: int = 1, item: Numeric = 0) -> _Set:
        
        """
        Pad the set by adding elements at the end.

        :param n_pad: Number of elements to add. Defaults to 1.
        :type n_pad: int
        :param item: Value to pad with. Defaults to 0.
        :type item: Numeric
        :return: This set with padded elements.
        :rtype: Self

        :Example:

        >>> s = _Set([1, 2, 3])
        >>> s.pad(2, 0).values
        [1.0, 2.0, 3.0, 0.0, 0.0]
        """
        
        self.vals = np.pad(self.vals, (0, n_pad), constant_values=item)
        return self

    def sort(self, type: Literal['<', '>', 'r'] = '<') -> _Set:
        
        """
        Sort elements in the specified order.

        :param type: Sort order. Options are:

            - ``'<'``: Ascending order.
            - ``'>'``: Descending order.
            - ``'r'``: Random shuffle.

            Defaults to ``'<'``.
        :type type: str
        :return: This set with sorted elements.
        :rtype: Self
        :raises ValueError: If type is not ``'<'``, ``'>'``, or ``'r'``.

        :Example:

        >>> s = _Set([3, 1, 4, 1, 5])
        >>> s.sort('<').values
        [1.0, 1.0, 3.0, 4.0, 5.0]
        """
        
        if type == '<':
            self.vals = np.sort(self.vals)
        elif type == '>':
            self.vals = np.sort(self.vals)[::-1]
        elif type == 'r':
            np.random.shuffle(self.vals)
        else:
            raise ValueError("Invalid order. Use '<', '>', or 'r'.")
        
        return self

    def interleave(self, other: ArrayLike = [0], step: int = 1) -> _Set:
        
        """
        Interleave elements from this set and another sequence.

        Alternates chunks of ``step`` elements from each sequence.

        :param other: The sequence to interleave with.
        :type other: ArrayLike
        :param step: Number of elements per chunk. Defaults to 1.
        :type step: int
        :return: A new set with interleaved elements.
        :rtype: _Set
        :raises ValueError: If step is not positive.

        :Example:

        >>> s = _Set([1, 2, 3, 4])
        >>> s.interleave(_Set([10, 20, 30]), step=1).values
        [1.0, 10.0, 2.0, 20.0, 3.0, 30.0, 4.0]
        """

        if step <= 0: raise ValueError("Step must be a positive integer")
        i = 0
        a = self.vals
        results = []

        if isinstance(other, _Set):
            b = other.vals

        while i < len(a) or i < len(b):
            if i < len(a):
                results.extend(a[i:i + step])
            if i < len(b):
                results.extend(b[i:i + step])
            i += step

        return type(self)(results)
    
    def round(self, decimals: int = 1) -> _Set:
        
        """
        Round values to a specified number of decimal places.

        Uses standard rounding (round half to even).

        :param decimals: Number of decimal places. Defaults to 1.
        :type decimals: int
        :return: This set with rounded values.
        :rtype: Self

        :Example:

        >>> s = _Set([1.234, 2.567, 3.891])
        >>> s.round(1).values
        [1.2, 2.6, 3.9]
        """
        
        self.vals = np.round(self.vals, decimals)
        return self
    
    def ceil(self) -> _Set:
        
        """
        Round values up to the nearest integer.

        :return: This set with ceiling values.
        :rtype: Self

        :Example:

        >>> s = _Set([1.1, 2.5, 3.9])
        >>> s.ceil().values
        [2.0, 3.0, 4.0]
        """

        self.vals = np.ceil(self.vals)
        return self
    
    def floor(self) -> _Set:
        
        """
        Round values down to the nearest integer.

        :return: This set with floor values.
        :rtype: Self

        :Example:

        >>> s = _Set([1.1, 2.5, 3.9])
        >>> s.floor().values
        [1.0, 2.0, 3.0]
        """

        self.vals = np.floor(self.vals)
        return self
    
    def filter(self, condition: np.ndarray | list | str , fill=None) -> _Set:
        
        """
        Filter elements based on a condition.

        :param condition: The filtering condition. Can be:

            - A boolean array or list.
            - A string expression using ``x`` for values and ``np`` for numpy.
            - A callable returning a boolean array.
        :type condition: np.ndarray | list | str | callable
        :param fill: Value to replace non-matching elements. If None,
            non-matching elements are removed. Defaults to None.
        :type fill: Numeric
        :return: This set with filtered elements.
        :rtype: Self

        :Example:

        >>> s = _Set([1, 2, 3, 4, 5, 6])
        >>> s.filter('x > 3').values
        [4.0, 5.0, 6.0]
        """

        if isinstance(condition, (list, np.ndarray)):
            mask = np.asarray(condition, dtype=bool)
        elif isinstance(condition, str):
            mask = eval(condition, {'x': self.vals, 'np': np})
        else:
            try:
                mask = condition(self.vals)
            except:
                raise ValueError("Not implemented")
            
        if fill is None:
            self.vals = self.vals[mask]
            
        else:
            self.vals[~mask] = fill
        
        return self
    
    def getseq(self, *,length: int = 2, type: Literal[None, 'wrap', 'fold', 'clip', 'rand', 'randnd'] = None, idx: tuple = None) -> list:
        
        """
        Generate a sequence of values using various indexing modes.

        :param length: Length of the sequence to generate. Defaults to 2.
        :type length: int
        :param type: Generation mode. Options are:

            - ``None``: Random selection with replacement.
            - ``'wrap'``: Cycle through indices.
            - ``'fold'``: Bounce back and forth.
            - ``'clip'``: Clamp indices to range.
            - ``'rand'``: Random with replacement.
            - ``'randnd'``: Random without replacement.

            Defaults to None.
        :type type: str
        :param idx: Index range ``[start, end]``. Defaults to None (full range).
        :type idx: tuple
        :return: List of generated values.
        :rtype: list

        :Example:

        >>> s = _Set([10, 20, 30, 40, 50])
        >>> s.getseq(length=6, type='wrap', idx=[0, 2])
        [10.0, 20.0, 30.0, 10.0, 20.0, 30.0]
        """
        
        data=[]

        if idx == None:
            idx = [0, len(self.vals)-1]

        if type == None:
            data.append(np.random.choice(self.vals, length, True))
            return data[0].tolist()
        
        elif type == 'wrap':
            for i in range(length):
                idVal = (i % abs((idx[1]+1) - idx[0])) + idx[0]
                data.append(self.vals[idVal])

        elif type == 'fold':
            index = idx[0]
            dir = 1
            for _ in range(length):
                data.append(self.vals[index])
                index += dir
                if index == idx[1] or index == idx[0]:
                    dir *= -1

        elif type == 'clip':
            for i in range(length):
                idVal = i + idx[0]
                if idVal >= idx[1]:
                    idVal = idx[1]
                data.append(self.vals[idVal])

        elif type == 'rand':
            data = np.random.choice(self.vals, length, True)

        elif type == 'randnd':
            if(length <= len(self.vals)):
                data = np.random.choice(self.vals, length, False)
            else:
                print('Invalid lenght, ecceded list lenght')

        return [x.item() for x in data]

    def getitems(self, idx: ArrayLike = None) -> list:
        
        """
        Retrieve items from the set by their indices.

        Supports nested lists of indices for flexible retrieval.

        :param idx: List of indices (may contain nested lists).
        :type idx: ArrayLike
        :return: List of values at the specified indices.
        :rtype: list
        :raises TypeError: If idx is not a list or contains invalid types.

        :Example:

        >>> s = _Set([10, 20, 30, 40, 50])
        >>> s.getitems([0, 2, 4])
        [10.0, 30.0, 50.0]
        """
        
        if not isinstance(idx, list):
            raise TypeError("ids must be a list")

        items = []

        for i in idx:
            if isinstance(i, list):
                for j in i:
                    items.append(self.vals[j].item())
            elif isinstance(i, int):
                items.append(self.vals[i].item())
            else:
                raise TypeError(f"Invalid index type: {type(i)}")

        return items

    def getids(self, items: list = None) -> list:
        
        """
        Find indices of specified values in the set.

        :param items: List of values to search for.
        :type items: list
        :return: List of lists, each containing indices where the
            corresponding item was found.
        :rtype: list[list[int]]
        :raises ValueError: If items is not a list.

        :Example:

        >>> s = _Set([10, 20, 30, 20, 40])
        >>> s.getids([20, 40])
        [[1, 3], [4]]
        """
        
        if isinstance(items, list):
            idx = []
            for i in items:
                idx.append(np.where(self.vals == i)[0].tolist())
            return idx
        else:
            raise ValueError(f'Incorrect fomat input: {id}')

    def split(self, *, idx: int | list[int] = None, items: float | list[float] = None, keep_separator: bool = True, split: Literal['before', 'after'] = 'after',) -> list["_Set"]:
        
        """
        Split the set into multiple sets at specified positions or values.

        Provide either ``idx`` or ``items``, not both.

        :param idx: Index or indices at which to split.
        :type idx: int | list[int]
        :param items: Value or values at which to split.
        :type items: float | list[float]
        :param keep_separator: If True, keep the separator element in the
            resulting parts. Defaults to True.
        :type keep_separator: bool
        :param split: Whether to split ``'before'`` or ``'after'`` the
            separator. Defaults to ``'after'``.
        :type split: Literal['before', 'after']
        :return: List of _Set instances representing the split parts.
        :rtype: list[_Set]
        :raises ValueError: If neither or both idx and items are provided,
            or if split mode is invalid.

        :Example:

        >>> s = _Set([1, 2, 3, 4, 5])
        >>> parts = s.split(idx=2)
        >>> [p.values for p in parts]
        [[1.0, 2.0, 3.0], [4.0, 5.0]]
        """

        if (idx is None) == (items is None):
            raise ValueError("Provide exactly one of 'idx' or 'items'")
        
        if split not in {"before", "after"}:
            raise ValueError("split must be 'before' or 'after'")

        vals = self.vals
        n = len(vals)
        parts: list[_Set] = []

        if idx is not None:
            try:
                indices = np.asarray(idx, dtype=int).reshape(-1)
            except Exception:
                raise TypeError("idx must be an integer or list of integers")

            if np.any(indices < 0) or np.any(indices >= n):
                raise ValueError("idx contains invalid indices")

            split_points = np.unique(indices)

        elif items is not None:
            items_arr = np.atleast_1d(items)

            if items_arr.size == 0:
                raise ValueError("items cannot be empty")

            mask = np.isin(vals, items_arr)
            if not mask.any():
                raise ValueError("items not found in set")

            split_points = np.flatnonzero(mask)

        start = 0

        for i in split_points:
            if i == 0:
                continue

            if split == 'before':
                cut = i
                next_start = i
            elif split == 'after':
                cut = i + 1
                next_start = cut

            if start < cut:
                parts.append(type(self)(vals[start:cut].tolist()))

            if keep_separator:
                start = next_start
            else:
                start = next_start + (0 if split == 'after' else 1)

        if start < n:
            parts.append(type(self)(vals[start:].tolist()))

        return parts
    
    def interpolation(self, other: _Set = None, step: int = 0, curve: float = 1) -> _Set:

        t = np.linspace(0, 1, step)
        t_curve = t ** curve
        result = self.vals + (other.vals - self.vals) * t_curve[:, np.newaxis]

        return [self.__class__(x).round(decimals=2) for x in result]
