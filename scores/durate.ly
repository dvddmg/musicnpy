
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
				  \numericTimeSignature
				  \time 4/4
				 <<
  				 { c'4 16 2 4 2 16 16 2 4 8 16 8 2 16 4 2 4 4 8 2 4 16 16 16  }
 				 >>
		}
		>>

	\layout {
		 }

	\midi { }
	}