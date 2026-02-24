
\version "2.24.3"
\language "english"
\header {
	tagline=""
	}
        
\paper {
	#(set-paper-size "a4landscape")
	top-margin=10
	bottom-margin=10
	left-margin=10
	right-margin=10
	}

\score {
	\new StaffGroup
		<<
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  } {
				 <<
  				 { as,16 fs,16 a16 c'16 e'16 fs'16 as'16 b'16 d''16 ds''16 f''16 fs''16 gs''16 as''16 b''16  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  } {
				 <<
  				 { ds,16 a,16 g16 cs'16 ds'16 g'16 a'16 c''16 cs''16 ds''16 e''16 fs''16 g''16 a''16 as''16 b''16  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  } {
				 <<
  				 { f,16 c16 fs16 d'16 ds'16 gs'16 c''16 cs''16 e''16 g''16 a''16 b''16  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  } {
				 <<
  				 { d,16 d16 e16 ds'16 cs'16 gs'16 g'16 cs''16 c''16 e''16 ds''16 g''16 fs''16 a''16 c'''16  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  } {
				 <<
  				 { gs,16 e16 d16 e'16 c'16 a'16 g'16 cs''16 b'16 f''16 ds''16 g''16 fs''16 as''16 a''16 c'''16  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  } {
				 <<
  				 { b,16 fs16 c16 f'16 b16 as'16 fs'16 d''16 b'16 f''16 ds''16 gs''16 fs''16 as''16 c'''16  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  } {
				 <<
  				 { g,16 g16 as,16 fs'16 as16 as'16 f'16 d''16 f''16 gs''16 as''16 c'''16  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  } {
				 <<
  				 { c,16 a16 g,16 fs'16 b'16 e'16 ds''16 a'16 fs''16 cs''16 gs''16 f''16 b''16 g''16 cs'''16  }
 				 >>
		}
		>>

	\layout {
		 }

	\midi { }
	}