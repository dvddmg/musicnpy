from musicnpy import *

a = _Set([1, 2, 3, 4])
print(a)
b = Scale.rand_int(12, min=-12, max=12, unique=True)
c = Scale.rand_flt(32, decimals=1)
d = Scale.n_time([1, 2, 3],10)
print(b)
print(c)
print(d)

print(d.contour)