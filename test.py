from musicnpy import *

a = Scale([1, 1, 1, 1, 1, 1], 72)
b = Scale([23, 13, 7, 0, -7, -24], 67)
z = Scale([-3, -2, -1, 1, 2, 3], 72)

c = a.interpolation(b, 7, 2)

d = _Set(c[-1]).interpolation(z, 7, 0.75)

c = [x.round(decimals=0).values for x in c]
d = [x.round(decimals=0).values for x in d]

Staff(c + d, filename='./scores/chords', format='pdf', size='a4landscape').make_file