
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
  				 { c' d' e' f' g' a' b'  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  } {
				 <<
  				 { < c' e' g' > < d' f' a' > < e' g' b' > < f' a' c'' > < g' b' d'' > < a' c'' e'' > < b' d'' f'' >  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  } {
				  \key ef \major
				 <<
  				 { c' d' ef' f' g' af' bf'  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  } {
				  \key ef \major
				 <<
  				 { < c' ef' g' > < d' f' af' > < ef' g' bf' > < f' af' c'' > < g' bf' d'' > < af' c'' ef'' > < bf' d'' f'' >  }
 				 >>
		}
		>>

	\layout {
		 }

	\midi { }
	}