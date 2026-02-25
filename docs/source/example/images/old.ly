
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
  				 { < d' g' c'' f'' >16 < d' g' c'' f'' >8 f'8 < g' c' d'' f'' >8 a'2 < g' c' d'' f'' >2 f'8 < g' c' d'' f'' >8 b'2 < d'' f' g'' c''' >2 f'8 < g' c' d'' f'' >8 cs''4 < g' c' d'' f'' >4 ds'4 < d'' f' g'' c''' >4 e'2 < d' g c'' f'' >2 fs'16 < c'' d' f'' g'' >16 gs'8 < d' g c'' f'' >8 as'8 < c'' d' f'' g'' >8 e'2 < d' g c'' f'' >2 as'16 < c'' d' f'' g'' >16 a'16 < g' c' d'' f'' >16 gs'4 < d' g c'' f'' >4 d'8 < c'' d' f'' g'' >8 cs''4 < g' c' d'' f'' >4 as'8 < c'' d' f'' g'' >8 cs''4 < g' c' d'' f'' >4 e'2 < d' g c'' f'' >2 g'8 < d'' f' g'' c''' >8 cs''8 < g' c' d'' f'' >8 fs'16 < c'' d' f'' g'' >16 a'2 < g' c' d'' f'' >2 c''4 < d' g c'' f'' >4 f'8 < g' c' d'' f'' >8 d'8 < c'' d' f'' g'' >8 f'16 < g' c' d'' f'' >16 e'16 < d' g c'' f'' >16 ds'4 < d'' f' g'' c''' >4 fs'2 < c'' d' f'' g'' >2 cs''4 < g' c' d'' f'' >4 a'16 < g' c' d'' f'' >16 as'8 < c'' d' f'' g'' >8 a'2 < g' c' d'' f'' >2 g'8 < d'' f' g'' c''' >8 g'8 < d'' f' g'' c''' >8 ds'8 < d'' f' g'' c''' >8 as'8 < c'' d' f'' g'' >8 cs''8 < g' c' d'' f'' >8 g'4 < d'' f' g'' c''' >4 a'2 < g' c' d'' f'' >2 as'8 < c'' d' f'' g'' >8 gs'8 < d' g c'' f'' >8 g'4 < d'' f' g'' c''' >4 c''8 < d' g c'' f'' >8 d'8 < c'' d' f'' g'' >8 e'16 < d' g c'' f'' >16 b'2 < d'' f' g'' c''' >2 < d' g' c'' f'' >8 ds'4 < d'' f' g'' c''' >4 c''8 < d' g c'' f'' >8 a'2 < g' c' d'' f'' >2 e'2 < d' g c'' f'' >2 b'2 < d'' f' g'' c''' >2 cs''4 < g' c' d'' f'' >4 g'8 < d'' f' g'' c''' >8 gs'4 < d' g c'' f'' >4 f'8 < g' c' d'' f'' >8 ds'8 < d'' f' g'' c''' >8 d'8 < c'' d' f'' g'' >8 b'16 < d'' f' g'' c''' >16 ds'8 < d'' f' g'' c''' >8 d'4 < c'' d' f'' g'' >4 fs'16 < c'' d' f'' g'' >16 d'4 < c'' d' f'' g'' >4 f'16 < g' c' d'' f'' >16 fs'2 < c'' d' f'' g'' >2 g'8 < d'' f' g'' c''' >8 fs'2 < c'' d' f'' g'' >2 < d' g' c'' f'' >8 d'8 < c'' d' f'' g'' >8 cs''4 < g' c' d'' f'' >4 d'8 < c'' d' f'' g'' >8 ds'8 < d'' f' g'' c''' >8 fs'16 < c'' d' f'' g'' >16 d'8 < c'' d' f'' g'' >8 g'4 < d'' f' g'' c''' >4 < d' g' c'' f'' >8 cs''8 < g' c' d'' f'' >8 b'16 < d'' f' g'' c''' >16 e'16 < d' g c'' f'' >16 cs''4 < g' c' d'' f'' >4 e'16 < d' g c'' f'' >16 ds'4 < d'' f' g'' c''' >4 b'2 < d'' f' g'' c''' >2 gs'4 < d' g c'' f'' >4 d'8 < c'' d' f'' g'' >8 cs''4 < g' c' d'' f'' >4 gs'8 < d' g c'' f'' >8 < d' g' c'' f'' >8 fs'16 < c'' d' f'' g'' >16 ds'8 < d'' f' g'' c''' >8 cs''8 < g' c' d'' f'' >8 gs'8 < d' g c'' f'' >8 g'4 < d'' f' g'' c''' >4 fs'2 < c'' d' f'' g'' >2 a'16 < g' c' d'' f'' >16 < d' g' c'' f'' >16 fs'2 < c'' d' f'' g'' >2 d'8 < c'' d' f'' g'' >8 a'16 < g' c' d'' f'' >16 gs'4 < d' g c'' f'' >4 as'8 < c'' d' f'' g'' >8 c''8 < d' g c'' f'' >8 d'8 < c'' d' f'' g'' >8  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  \clef bass
				  } {
				 <<
  				 { < c g d' a' >16 c,2 < c, g, d, a >2 cs,8 < g, c d, a >8 g,4 < c g a, d' >4 fs,8 < c d g, a >8 < c g d' a' >8 b,8 < c g a, d' >8 a,8 < g, c d, a >8 f,16 < g, c d, a >16 b,8 < c g a, d' >8 fs,8 < c d g, a >8 gs,2 < c, g, d, a >2 ds,2 < c g a, d' >2 e,8 < c, g, d, a >8 a,16 < g, c d, a >16 cs,8 < g, c d, a >8 e,16 < c, g, d, a >16 d,4 < c d g, a >4 cs,8 < g, c d, a >8 gs,16 < c, g, d, a >16 b,8 < c g a, d' >8 as,2 < c d g, a >2 cs,8 < g, c d, a >8 e,8 < c, g, d, a >8 g,4 < c g a, d' >4 a,8 < g, c d, a >8 ds,2 < c g a, d' >2 as,16 < c d g, a >16 b,4 < c g a, d' >4 gs,2 < c, g, d, a >2 ds,16 < c g a, d' >16 cs,8 < g, c d, a >8 e,8 < c, g, d, a >8 ds,2 < c g a, d' >2 cs,8 < g, c d, a >8 gs,2 < c, g, d, a >2 ds,2 < c g a, d' >2 g,4 < c g a, d' >4 f,16 < g, c d, a >16 b,8 < c g a, d' >8 e,8 < c, g, d, a >8 d,4 < c d g, a >4 b,8 < c g a, d' >8 f,2 < g, c d, a >2 fs,8 < c d g, a >8 < c g d' a' >8 d,4 < c d g, a >4 a,8 < g, c d, a >8 cs,8 < g, c d, a >8 as,16 < c d g, a >16 ds,2 < c g a, d' >2 fs,8 < c d g, a >8 e,16 < c, g, d, a >16 ds,16 < c g a, d' >16 cs,8 < g, c d, a >8 ds,16 < c g a, d' >16 c,2 < c, g, d, a >2 < c g d' a' >8 d,4 < c d g, a >4 g,4 < c g a, d' >4 e,8 < c, g, d, a >8 g,4 < c g a, d' >4 b,8 < c g a, d' >8 as,16 < c d g, a >16 d,4 < c d g, a >4 cs,8 < g, c d, a >8 ds,2 < c g a, d' >2 < c g d' a' >8 fs,8 < c d g, a >8 gs,16 < c, g, d, a >16 b,8 < c g a, d' >8 d,4 < c d g, a >4 gs,16 < c, g, d, a >16 a,8 < g, c d, a >8 d,4 < c d g, a >4 gs,2 < c, g, d, a >2 a,8 < g, c d, a >8 a,8 < g, c d, a >8 ds,2 < c g a, d' >2 c,16 < c, g, d, a >16 ds,2 < c g a, d' >2 gs,2 < c, g, d, a >2 < c g d' a' >8 c,16 < c, g, d, a >16 a,16 < g, c d, a >16 d,4 < c d g, a >4 < c g d' a' >16 e,8 < c, g, d, a >8 g,4 < c g a, d' >4 gs,2 < c, g, d, a >2 cs,8 < g, c d, a >8 cs,8 < g, c d, a >8 f,16 < g, c d, a >16 a,8 < g, c d, a >8 d,4 < c d g, a >4  }
 				 >>
		}
		>>

	\layout {
		 }

	\midi { }
	}