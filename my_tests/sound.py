from musicnpy import *
import fluidsynth
import numpy as np

fs = fluidsynth.Synth()
fs.start(driver = 'coreaudio')
sfid = fs.sfload(r'/Users/davide/Downloads/Soundfont/FluidR3_GM/FluidR3_GM.sf2') 
instr = [13, 12]

a = Scale.new(ScaleModel.maj, 1).getseq(length=75,type='rand')
print(a)
c = Chord([-12, -4, -2, 0, 3, 5, 12, 16, 20, 30, 35, 39, 40, 45], 40)
seq = PitchSequence((c, c, a, c, c, c, c, a, c, c, c, a)).out

c = Chord([-7, 2, 9], 36)
b = Chord.new(ChordModel.aug, 60)

c = c.interpolation(b, 100, 3.9, 0)


c = np.asanyarray(c, int).tolist()

dur = Pattern([16, 8, 4]).gen(100, type='fold')

b = Staff((seq, c), (16, dur), (90, 90)).play(bpm=120,instrID=instr)