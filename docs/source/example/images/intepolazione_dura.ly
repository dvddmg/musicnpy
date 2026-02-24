
\version "2.24.3"
\language "english"
\header {
	tagline=""
	}
        #(set! paper-alist (cons '("mio formato" . (cons (* 230 mm) (* 40 mm))) paper-alist) )
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
				  \key ef \major
				  \numericTimeSignature
				  \time 3/4
				 <<
  				 { < c'' ef'' g'' >4 < c' ef' gf' >4 < df' e' g' >4 < d' f' af' >4 < ef' gf' bf' >4 < f' af' c'' >4 < g' bf' d'' >4 < bf' df'' e'' >4 < c'' ef'' g'' >4 < c' ef' gf' >4 < c'' ef'' g'' >4 < c' ef' gf' >4 < c'' ef'' g'' >4 < c' ef' gf' >4 < c'' ef'' g'' >4 < bf' df'' e'' >4 < g' bf' d'' >4 < f' af' c'' >4 < ef' gf' bf' >4 < d' f' af' >4 < df' e' g' >4 < c' ef' gf' >4 < c'' ef'' g'' >4  }
 				 >>
		}
		>>

	\layout {
		 }

	\midi { }
	}