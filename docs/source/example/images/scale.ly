
\version "2.24.3"
\language "english"
\header {
	tagline=""
	}
        #(set! paper-alist (cons '("mio formato" . (cons (* 150 mm) (* 50 mm))) paper-alist) )
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
  				 { c'4 d'4 e'4 f'4 g'4 a'4 b'4 c'''4 < c' e' g' >4 < d' f' a' >4 < e' g' b' >4 < f' a' c'' >4 < g' b' d'' >4 < a' c'' e'' >4 < b' d'' f'' >4 < c'' e'' g'' >4  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  } {
				  \key ef \major
				 <<
  				 { c'4 d'4 ef'4 f'4 g'4 af'4 bf'4 c4 < c' ef' g' >4 < d' f' af' >4 < ef' g' bf' >4 < f' af' c'' >4 < g' bf' d'' >4 < af' c'' ef'' >4 < bf' d'' f'' >4 < c'' ef'' g'' >4  }
 				 >>
		}
		>>

	\layout {
		 }

	\midi { }
	}