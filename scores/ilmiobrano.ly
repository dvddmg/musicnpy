
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
  				 { e' f' c' f' c' e' e' d' f' d' d' d' e' g' c' f' e' d' e' c' g' d' g' g' d' a' a' b' a' d' f' g' g' d' d' c' b' d' c' c' e' g' e' g' b' g' d' f' g' d' b' d' d' f' b' a' f' g' b' c' d' d' a' b' e' d' f' f' f' g' c' a' f' e' d' d' f' g' a' b' a' f' b' f' e' g' b' e' f' e' d' g' a' b' g' a' c' b' a' f'  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  \clef bass
				  } {
				 <<
  				 { r  r  < fs,, gs,, b,, c, cs, d, ds, > r  r  < cs,, d,, e,, f,, f,, fs,, g,, > r  < b,, d, f, g, gs, a, as, > < c f c' ds' f' gs' b' > r  < f, a, f g c' c' e' > < b, ds b d' e' g' as' > < b ds' as' cs'' ds'' fs'' a'' > r  < ds,, e,, g,, gs,, a,, as,, b,, > < c, d, gs, a, c c ds > < as, d as c' ds' f' a' > r  r  r  r  r  < fs, a, cs ds e fs gs > < fs, a, fs g c' c' f' > < ds, f, as, b, cs d e > r  r  r  r  < a,, b,, ds, e, f, fs, gs, > < gs,, b,, d, ds, e, f, fs, > r  r  < fs, a, fs gs c' cs' f' > r  r  < gs, as, f g as as cs' > r  r  < e, g, b, cs d e fs > r  r  r  < as d' a' c'' d'' f'' g'' > r  < as, d g a b cs' ds' > r  < gs, c gs b d' e' g' > < a, cs a b d' e' gs' > r  < ds,, e,, g,, g,, gs,, a,, as,, > r  r  < b, e b d' e' g' as' > r  r  < b, cs a b d' ds' fs' > < d, e, d ds gs a cs' > r  r  < f,, fs,, a,, as,, as,, c, cs, > r  r  r  < f, g, as, c cs d ds > r  < fs, gs, b, cs cs ds e > < cs, ds, fs, g, gs, gs, as, > r  r  r  < ds, fs, as, b, cs d e > r  r  r  r  < c f c' ds' f' gs' b' > r  < ds, fs, ds e a as d' > < d, e, a, as, cs cs e > r  < c f c' ds' f' gs' b' > r  r  r  < f, gs, cs ds f fs a > r  r  r  < gs,, as,, cs, ds, ds, f, fs, > < as, cs g a cs' cs' e' > r  < f,, g,, as,, as,, b,, c, d, > r  < a d' a' c'' d'' f'' gs'' > r  < f,, g,, as,, as,, b,, c, d, > r  r  < d,, ds,, e,, f,, fs,, fs,, g,, >  }
 				 >>
		}
		>>

	\layout {
		 }

	\midi { }
	}