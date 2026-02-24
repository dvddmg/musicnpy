******************************
Topyly
******************************

.. currentmodule:: musicnpy.topyly

Introduction
===================
This moodule produde hte functionality to convert musical data into LilyPond format, also including exporting to MIDI and graphical format.
It also provides some tools for playing with FluidSynth.

_Map Class
===================

``_Map`` is a class that provides methods for mapping musical data from python to LilyPond format.
It's the base class for the next classes.

.. automethod:: _Map.__init__

_Print Class
===================

``_Print`` is a class that save these files:
        • lilypond file (.ly)
        • MIDI file (.mid)
        • graphic file (.pdf or .png)

.. automethod:: _Print.__init__
.. autoattribute:: _Print.print_out
.. autoattribute:: _Print.make_file

Staff Class
===================

``Staff`` is a rappresentation of a musical staff for lilypond. It can be used to create a musical score with the given musical data.

.. automethod:: Staff.__init__
.. autoattribute:: Staff.out
.. automethod:: Staff.play

Score Class
===================

``Score`` rapresentes a musical score for lilypond. It can be used to create a musical score with the given musical data.

.. automethod:: Score.__init__
.. automethod:: Score.sei_libero

Functions
===================

.. autofunction:: tonalita
.. autofunction:: mapPitch
.. autofunction:: mapDur
.. autofunction:: mapVel
.. autofunction:: mapExp
.. autofunction:: nDim
.. autofunction:: l_mod
.. autofunction:: l_zero
.. autofunction:: dflt
.. autofunction:: selmode
.. autofunction:: getmaxsize
.. autofunction:: dur2sec
.. autofunction:: note
.. autofunction:: voice
.. autofunction:: voices