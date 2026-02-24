
\version "2.24.3"
\language "english"
\header {
	tagline=""
	}
        #(set! paper-alist (cons '("mio formato" . (cons (* 250 mm) (* 100 mm))) paper-alist) )
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
  				 { c'4 d'4 ds'4 f'4 fs'4 gs'4 a'4 b'4 g'4 d'4 ds'4 f'4 fs'4 gs'4 a'4 b'4 g'4 d'4 ds'4 f'4 fs'4 gs'4 a'4 fs''4 g'4 a'4 ds'4 f'4 fs'4 gs'4 a'4 fs''4 g'4 a'4 ds'4 f'4 fs'4 gs'4 f''4 fs''4 g'4 a'4 b'4 f'4 fs'4 gs'4 f''4 fs''4 g'4 a'4 b'4 f'4 fs'4 e''4 f''4 fs''4 g'4 a'4 b'4 c''4 fs'4 e''4 f''4 fs''4 g'4 a'4 b'4 c''4 d''4 e''4 f''4 fs''4  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  \clef bass
				  } {
				 <<
  				 { < c' ds' fs a' >2 < c' ds' d' a' >2 < c' b' d' a' >2 < c' b' d' fs'' >2 < d' f gs' b' >2 < a' f gs' b' >2 < a' c' gs' b' >2 < a' c' e'' b' >2 < ds' fs' a c'' >2 < ds' fs' a a'' >2 < ds' fs' fs' a'' >2 < ds' d'' fs' a'' >2 < f' gs b' d'' >2 < f' e' b' d'' >2 < c'' e' b' d'' >2 < c'' e' g'' d'' >2 < fs' a' c' ds'' >2 < d'' a' c' ds'' >2 < d'' fs'' c' ds'' >2 < d'' fs'' a' ds'' >2 < gs' b d'' f'' >2 < e'' b d'' f'' >2 < e'' b d'' d''' >2 < e'' g' d'' d''' >2 < a' c'' ds' fs'' >2 < a' c'' b' fs'' >2 < a' gs'' b' fs'' >2 < f'' gs'' b' fs'' >2 < b' d' f'' gs'' >2 < b' d' f'' e''' >2 < b' d' cs''' e''' >2 < b' as' cs''' e''' >2 < c' ds' fs a' >2 < c' ds' fs fs'' >2 < c' ds' d' fs'' >2 < c' b' d' fs'' >2  }
 				 >>
		}
		>>

	\layout {
		 }

	\midi { }
	}