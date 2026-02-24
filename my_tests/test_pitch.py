from musicnpy import *
import numpy as np
import random as rnd
# ========================================== _PSet TEST
# a = _PSet([0, 2, 4, 5, 7, 9, 11, 12], 60)

# print(a.pitches)
# print(f'delta = {a.deltas}')
# print(f'intervalli = {a.intervals}')

# print(f'frequenze = {a.to_freq()}')

# b = _PSet.from_freq([440, 265, 220, 880])
# print(b)


# ========================================== Scale TEST
# b = Scale([0, 2, 4, 5, 7, 9, 11], 60)

# d = Scale([0, 0.5, 1.5, 2, 7.15], 60)/3
# print(d)

# a = Scale([0, 4, 6, 8, 9, 12], 60, )

# d = Scale.new(ScaleModel.maj, 48)
# print(d.harmo)
# print(d.root)
# print(d.pitches)
# print(d.intervals)
# print(d.diatonic)
# d.harmonize
# d.chords[0]
# print(d.chords[0])
# for i in d.chords:
#     print(i.n_inversion(2))

# print(d.chords[0].n_inversion().pitches)

# print(d.voicing(3))

# ========================================== Chord TEST
# a = Chord([0, 3, 7], 60)
# print(a.pitches)
# print(a.intervals)

# p = Chord.new(ChordModel.dim7, 64)
# print(p)
# print(p.root)
# print(p.pitches)
# print(p.intervals)


# a = Chord([0, 3, 4, 7, 9], 60)
# print(a)
# print(a.first_inv)
# print(a.second_inv)
# print(a.n_inversion([1, 1, 1, 1]))
# print(a)
# Modificato come segue
# Chord([0, 1, 2, 3, 4, 5], 60).n_inversion(3)

# ================================ RM test
# carr = 440
# mod = 5
# s1, s2 = abs(carr-mod), abs(carr+mod)
# print(s1, s2)

# a = Chord([0, 4, 7, 11, 12, 15, 19, 24, 48], 73).to_freq()
# a = Chord([0, 4, 7, 11], 60).to_freq()
# mod = 4
# for i in range(len(a)):
#     a[i] = round(a[i], 2)

# out = []
# for f in enumerate(a):
#     out.append(f[1] - mod)
#     out.append(f[1] + mod)

# print(out)

# rmChord = Chord.from_freq(out)
# print(rmChord)

# accordoRM = Chord.from_freq(out)
# print(accordoRM)
# print(Chord.from_freq([220, 440]))

# a = Spectra([55, 110, 440])
# b = a.ring_mod(21.234)
# b = Chord.from_freq(b).micro_quanta(1)

# print(b)

# a = Spectra.harm_series(65, 16, 1.853)
# b = a.ring_mod(21.1234)
# crd = Chord.from_freq(b).micro_quanta(1)
# scl = Scale.from_freq(b).micro_quanta(1)

# seq = PitchSequence((crd, scl)).out
# dur = [2, 16]
# voce = Staff(seq, dur, 90).out
# Score(voce, filename='scores/rm').make_file


#__________________________

# chords = [ChordModel.aug,
#           ChordModel.dim7,
#           ChordModel.german_aug6,
#           ChordModel.quintal,
#           ChordModel.dom_b9,
#           ChordModel.quartal] # max 12

# roots = Scale.new(ScaleModel.chromatic, 36)

# mods = [0.4, 12, 2.523, 155.1234, 550.123, 55.12345]

# seq_odd = []
# seq_even = []

# for i in range(len(chords)):
#     a = Chord.new(chords[i], roots[i])
#     rm = Spectra.to_ring_mod(a, mods[i])
#     rmChord = Chord.from_freq(rm.vals).micro_quanta(1)
#     seq_odd.append(Chord(rmChord.odd).to_range(72, 96))
#     seq_even.append(Chord(rmChord.even).to_range(36, 60))

# seq_odd = PitchSequence(seq_odd).out
# seq_even = PitchSequence(seq_even).out

# a = Staff(seq_odd, 4, 90).out
# b = Staff(seq_even, 4, 90, clef='bass').out

# Score((a, b), filename='scores/rm').make_file


#___________________________

# N_HARMS = 8

# a = Spectra.harm_series(55, N_HARMS, 1)
# b = Spectra.harm_series(75, N_HARMS, 1.5784)

# seq = []

# for i in enumerate(a):
#     id, item = i[0], i[1]
#     ring = b.ring_mod(a[id]/3.1234)
#     scale = Scale.from_freq(ring.values).micro_quanta(1).to_range(36, 92).unique()
#     voce = Staff(scale.values, 16, 90).out
#     seq.append(voce)

# Score(tuple(seq), filename='scores/rm_scales').make_file


# doMaj = Scale.new(ScaleModel.maj, 60)
# doMin = Scale.new(ScaleModel.minNat, 60)

# doScale = Staff(doMaj.pitches).out
# doHarmo = Staff([i.pitches for i in doMaj.harmonize]).out
# doMinScale = Staff(doMin.pitches, key='ef').out
# doMinHarmo = Staff([i.pitches for i in doMin.harmonize], key='ef').out

# # print(doMaj, doMin)
# Score((doScale, doHarmo, doMinScale, doMinHarmo), filename='./scores/scale').make_file




# ================================== SEQUENCE TEST


# doMaj = Scale.new(ScaleModel.maj, 60)
# doMin = Scale.new(ScaleModel.minNat, 60)

# seq = PitchSequence((doMaj, doMin))
# print(seq.seq)


# PitchSequence(([0, 1, 2], 48, Scale.new(ScaleModel.maj, 60), Chord([48, 75, 92], 0))).out

# PitchSequence(([0, 1, 2])).out
# PitchSequence((1, 2, 3)).out
# PitchSequence((Chord.new(ChordModel.maj, 60))).out
# PitchSequence((Scale.new(ScaleModel.maj, 60))).out
# print(PitchSequence((Scale.new(ScaleModel.maj, 60).harmonize)).out)










# doMaj = Scale.new(ScaleModel.maj, 60)
# doMin = Scale.new(ScaleModel.minNat, 60)

# seq_1 = PitchSequence((doMaj, 72, doMaj.harmonize, Chord.new(ChordModel.maj, 72))).out
# seq_2 = PitchSequence((doMin, 48, doMin.harmonize, Chord.new(ChordModel.min, 72))).out

# staff_1 = Staff(seq_1).out
# staff_2 = Staff(seq_2, key='ef').out
# Score((staff_1, staff_2), filename='./scores/scale').make_file


# a = Chord([-12, -7, 0, 3, 5, 8, 11], 60)
# b = Chord([-11, -9, 1, 2, 8, 7, 12], 48)

# interp = a.interpolation(b, 100, 2.5)

# seq_3 = PitchSequence(interp).out
# seq_3 = np.round(seq_3).tolist()

# Staff(seq_3, filename='./scores/interpolazionelunga').make_file



 
# a = Chord([-12, -7, 0, 3, 5, 8, 11], 60)
# b = Chord([-11, -9, 1, 2, 8, 7, 12], 48)

# interp = a.interpolation(b, 100, 2.5)


# scala = Scale.new(ScaleModel.maj, 48)
# scalaUp = scala.shift(12)
# scala = scala.concat(scalaUp)

# NUMERO_BATTUTE = 25
# NUMERO_NOTE = 50
# NUMERO_BEAT = 25*4
# PAUSA = -1
# RISERVA_ARMONICA = PitchSequence(interp)

# voice_1 = [] # melodia
# voice_2 = [] # accompagnamento

# for i in range(NUMERO_BEAT):
#     nota = rnd.choice(scala)
#     voice_1.append(nota)

#     if rnd.randint(0, 100) > 50:
#         accordo = rnd.choice(RISERVA_ARMONICA)
        
#         if rnd.randint(0, 100) > 20:
#             accordo.n_inversion(rnd.randint(2, 4))
#         if rnd.randint(0, 100) > 30:
#             accordo *= rnd.randint(500, 2000)/2000
#             accordo.shift(12)
            
        
#         accordo.round(0)
#         voice_2.append(accordo.values)
#     else:
#         voice_2.append(PAUSA)


# voce = Staff(voice_1).out
# acco = Staff(voice_2, clef='bass').out

# Score((voce, acco), filename='./scores/ilmiobrano').make_file




a = Chord(ChordModel.dim, 60)
b = Chord(ChordModel.min, 72)

interp = a.interpolation(b, 8, 1.5, 0)
reverseInterp = interp[::-1]

seq = PitchSequence((b, interp, a, b, a, b, a, reverseInterp, b))

o = Staff(seq.out, t_sig='3/4', key='ef').out
Score(o, filename='./scores/intepolazione_dura').make_file











# PITCH CON DURATE






# BATTUTE = 25
# N_BEAT = 5
# PAUSA = -1

# scala = Scale.new(ScaleModel.maj, root=65) # fa maggiore
# harmo = scala.harmonize
# pattr = Pattern([8, 4, 2])

# voice_1 = []
# voice_2 = []

# durs_1 = []
# durs_2 = []

# for i in range(BATTUTE):
#     for i in range(N_BEAT):

#         if rnd.randint(0, 100) > 20:
#             nota = rnd.choice(scala)
#             voice_1.append(nota)

#             durata = rnd.choice(pattr.vals)
#             durs_1.append(durata)
            

#             # if rnd.randint(0, 100) > 50:
#             #     durPass = durata*2
#             #     abbell = rnd.choice(scala)

#             #     voice_1.append(abbell)
#             #     durs_1.append(durPass)

#             #     voice_2.append(PAUSA)
#             #     durs_2.append(durPass)

#             idChord = scala.getids([nota])[0][0]
#             chord = harmo[idChord] - 24
            
#             inv_choice = rnd.randint(0, 100)

#             if inv_choice < 20:
#                 chord = chord
#             if inv_choice >= 20 and inv_choice <= 60:
#                 chord = chord.first_inv
#             if inv_choice > 60:
#                 chord = chord.second_inv

#             voice_2.append(chord.values)
#             durs_2.append(durata)
#         else:
#             # meete una pausa
#             voice_1.append(PAUSA)
#             voice_2.append(PAUSA)

# dx = Staff(voice_1, durs_1, t_sig='5/4', key='f').out
# sx = Staff(voice_2, durs_2, t_sig='5/4', key='f', clef='bass').out

# Score((dx, sx), filename='./scores/faMaggiore').make_file



# a = Chord.rand_int(7, 0, 127)
# print(a)
# b = a.to_range(60, 72)
# print(b)


# a = Chord.rand_flt(4, 60.1234, 89.1234, 6)
# print(a)
# a.micro_quanta(8)
# print(a)

# a = Scale.new(ScaleModel.maj, 0).getseq(length=100, type='rand')
# b = a.scale_quanta(ScaleModel.minNat)
# print(a)
# print(b)
# Staff(seq).make_file

# a = Scale.new(ScaleModel.maj, 60).filter([0, 1, 1, 1, 0, 1, 0], 0)
# print(a)

# a = Scale([0, 1, 3, 4, 5, 6, 7], 36)
# b = Scale([0, 1, 3, 4, 5, 6, 7], 60)

# up = b.morphing(a, 'up')
# down = b.morphing(a, 'down')
# rand = a.morphing(b, 'rand')
# chiasmo = a.morphing(b, 'chiasm')

# for i in up:print(i)
# print('\n')
# for i in down:print(i)
# print('\n')
# for i in rand: print(i)
# print('\n')
# for i in chiasmo: print(i)



a = Spectra.harm_series(55, 8, 1.02)

# chord = Chord(a.values)
# scale = Scale(a.values, 0)

# chord.micro_quanta(1)

# seq_1 = PitchSequence((chord, scale)).out

# Staff(seq_1, 4, 90, filename='scores/harmonic', clef='bass').make_file