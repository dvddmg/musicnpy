
\version "2.24.3"
\language "english"
\header {
	tagline=""
	}
        #(set! paper-alist (cons '("mio formato" . (cons (* 150 mm) (* 100 mm))) paper-alist) )
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
  				 { ds e f fs g gs a  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  } {
				 <<
  				 { ds e f fs g gs a  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  } {
				 <<
  				 { e,, e,, f,, f,, fs,, fs,, g,, g,, gs,, gs,, a,, a,, as,, as,,  }
 				 >>
		}
		>>

	\layout {
		 }

	\midi { }
	}