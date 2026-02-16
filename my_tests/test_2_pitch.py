from musicnpy import *

# a = Scale([0, 2, 4, 5, 7, 9, 11], 48)
# print(a)

b = Scale.new(ScaleModel.minNat, 56)
# print(a.pitches)
# print(a.root)
# print(a.to_freq())
# print(a.diatonic)
# print(a.harmonize)

a = Chord([0, 4, 7, 8, 9, 10, 12], 60)
# print(a)
# print(a.first_inv)
# print(a.second_inv)
# print(a.n_inversion(5))
# b = Chord.new(ChordModel.dim7, 48)
# print(b)

# _Set(a.pitches).sort('r')

b = a.acc.sort('r') + 12
print(b)

Staff([b.pitches], filename='./scores/accordo').make_file