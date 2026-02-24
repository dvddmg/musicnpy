
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
  				 { e' g' g' e' a' d' c' f' b' a' e' c' e' b' b' d' b' d' e' g' a' c' g' d' b' b' b' d' f' b' e' a' f' f' a' b' a' a' d' a' c' f' c' b' c' c' f' g' a' d' b' b' e' g' a' b' b' f' f' d' f' a' g' c' e' d' c' a' f' e' g' e' a' a' d' a' a' f' c' f' d' a' c' f' f' a' f' a' g' a' g' b' g' c' g' a' f' c' d' c'  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  \clef bass
				  } {
				 <<
  				 { r  r  < e, fs, b, cs ds e fs > r  r  r  r  r  < d, e, gs, a, b, c d > r  < c f c' ds' f' gs' b' > r  < cs e b c' ds' e' gs' > r  < c f c' ds' f' gs' b' > r  < ds, fs, ds f as as d' > r  r  < a, cs a c' ds' f' gs' > < ds,, f,, g,, gs,, a,, as,, b,, > r  < g,, a,, c, cs, d, ds, e, > r  r  < c,, cs,, ds,, e,, f,, f,, fs,, > r  r  < c f c' ds' f' gs' b' > r  r  r  r  < e, fs, c d e f gs > r  r  r  < g, b, g a cs' d' fs' > r  < as,,, as,,, b,,, b,,, c,, c,, c,, > r  < a,, as,, ds, e, fs, fs, gs, > < g, b, g as cs' ds' fs' > r  r  < c f c' ds' f' gs' b' > r  < d fs b d' ds' fs' gs' > r  r  < as,, c, e, f, g, g, a, > r  r  r  < ds, fs, b, c d ds f > r  < g, b, g a cs' d' fs' > < gs, b, e fs gs as c' > r  < a d' a' c'' ds'' f'' gs'' > r  < ds,, f,, g,, gs,, a,, as,, b,, > r  < e, g, e f as as ds' > < d fs b cs' ds' f' gs' > r  r  < g c' fs' a' as' cs'' e'' > < gs cs' g' as' c'' d'' f'' > < cs ds b c' f' f' a' > r  r  < f a e' fs' as' b' ds'' > < f,, fs,, g,, gs,, gs,, a,, as,, > r  r  < as,,, as,,, b,,, b,,, b,,, b,,, b,,, > r  < b, e b d' f' g' as' > < fs as f' g' as' c'' d'' > < as, d g a b c' ds' > < b, e b d' e' g' as' > r  < as ds' as' c'' d'' f'' gs'' > < ds,, e,, gs,, a,, b,, b,, cs, > < g,, a,, c, cs, d, e, f, > r  < gs,, as,, d, ds, f, fs, gs, > r  < cs ds b c' f' f' a' > < gs,, as,, cs, d, e, e, fs, > < c e c' d' f' g' b' > < ds, f, as, b, d ds f > < a, c f g gs as c' > < e,, f,, g,, g,, gs,, a,, as,, > < a,, b,, ds, e, f, fs, gs, > < c f c' ds' f' gs' b' > < gs,, as,, cs, d, ds, e, f, > r  < c e c' d' f' g' b' >  }
 				 >>
		}
		>>

	\layout {
		 }

	\midi { }
	}