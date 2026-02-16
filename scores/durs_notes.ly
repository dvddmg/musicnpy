
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
  				 { gs8 fs2 d8 as2 gs8 c16  }
 				 >>
		}
		>>

	\layout {
		 }

	\midi { }
	}