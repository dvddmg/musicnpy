
\version "2.24.3"
\language "english"
\header {
	tagline=""
	}
        #(set! paper-alist (cons '("mio formato" . (cons (* 100 mm) (* 55 mm))) paper-alist) )
\paper {
	#(set-paper-size "mio formato")
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
  				 { < >4 < cs'' f'' a'' >4 < cs'' ds'' a'' a'' >4 < ds'' ds'' cs'' ds'' >4 < ds'' a'' g'' f'' >4 < cs'' b'' f'' g'' ds'' >4  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  \clef bass
				  } {
				 <<
  				 { < c, c, e, e, gs, gs, >4 < as, e, fs, gs, c >4 < fs, fs, c c >4 < as e, gs, gs, >4 < as, e, gs, e, fs, fs, >4 < c, gs c' >4  }
 				 >>
		}
		>>

	\layout {
		 }

	\midi { }
	}