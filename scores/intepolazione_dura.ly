
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
				  \key ef \major
				  \numericTimeSignature
				  \time 3/4
				 <<
  				 { < c'' ef'' g'' > < c' ef' gf' > < df' e' g' > < d' f' af' > < ef' gf' bf' > < f' af' c'' > < g' bf' d'' > < bf' df'' e'' > < c'' ef'' g'' > < c' ef' gf' > < c'' ef'' g'' > < c' ef' gf' > < c'' ef'' g'' > < c' ef' gf' > < c'' ef'' g'' > < bf' df'' e'' > < g' bf' d'' > < f' af' c'' > < ef' gf' bf' > < d' f' af' > < df' e' g' > < c' ef' gf' > < c'' ef'' g'' >  }
 				 >>
		}
		>>

	\layout {
		 }

	\midi { }
	}