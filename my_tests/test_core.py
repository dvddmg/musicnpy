from musicnpy import *

a = _Set([1, 2, 3, 4], 60)
a.invert(63)
b = _Set(a.deltas, 50)


c = Scale([0, 1, 2, 3, 4], 60)
c * 20
print(c.deltas)