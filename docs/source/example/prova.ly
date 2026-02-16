
\version "2.24.3"
\language "english"
\header {
	tagline=""
	}
        #(set! paper-alist (cons '("mio formato" . (cons (* 220 mm) (* 50 mm))) paper-alist) )
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
  				 { < fs' as' cs'' > < c ds g > < c ds g > < cs e gs > < d f a > < e g b > < g as d' > < b d' fs' > < e' gs' b' > < as' d'' f'' > < fs'' as'' cs''' > < fs'' as'' cs''' > < fs'' as'' cs''' > < fs'' as'' cs''' > < fs'' as'' cs''' > < fs'' as'' cs''' > < f'' a'' c''' > < d'' fs'' a'' > < as' d'' f'' > < d' f' a' > < c ds g > < c' ds' g' >  }
 				 >>
		}
		>>

	\layout {
		 }

	\midi { }
	}