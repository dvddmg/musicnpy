
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
				  \key f \major
				  \numericTimeSignature
				  \time 5/4
				 <<
  				 { r 4 g'2 c''4 r 4 a'8 c''2 d''8 bf'2 g'2 r 2 g'2 r 2 e''2 d''8 f'2 e''8 d''8 c''2 r 8 f'2 e''2 d''4 g'2 e''2 d''2 a'2 g'8 a'4 r 2 r 8 f'8 g'8 r 4 g'2 e''2 r 8 e''4 g'2 r 2 e''2 d''4 f'8 f'2 d''2 g'8 r 2 f'8 a'8 g'4 g'2 r 8 e''4 bf'8 bf'8 a'8 g'2 f'8 a'8 c''2 c''8 c''4 c''8 r 4 c''2 a'4 e''8 a'4 c''4 r 4 r 8 c''4 r 4 r 8 f'2 r 2 r 2 d''8 g'2 g'8 c''8 f'2 g'2 a'4 c''2 r 2 g'2 f'8 d''2 g'4 bf'4 a'2 e''4 c''2 a'8 g'8 r 2 g'8 r  f' bf' g' a' bf' c'' d'' d'' r  r  bf' f' a' r  g' a' d'' d'' e'' f' r  d'' f' d'' r  r  bf'  }
 				 >>
		}
		\new Staff \with {
				  midiInstrument="acoustic grand"
				  \clef bass
				  } {
				  \key f \major
				  \numericTimeSignature
				  \time 5/4
				 <<
  				 { r 4 < bf, d g >2 < e g c' >4 r 4 < c e a >8 < c e g >2 < a d' f' >8 < d f bf >2 < bf, d g >2 r 2 < bf, d g >2 r 2 < bf e' g' >2 < a d' f' >8 < a, c f >2 < g bf e' >8 < f a d' >8 < c e g >2 r 8 < c f a >2 < g bf e' >2 < d f a >4 < d g bf >2 < bf e' g' >2 < d f a >2 < c e a >2 < d g bf >8 < a, c e >4 r 2 r 8 < f, a, c >8 < g, bf, d >8 r 4 < d g bf >2 < bf e' g' >2 r 8 < bf e' g' >4 < d g bf >2 r 2 < g bf e' >2 < f a d' >4 < f, a, c >8 < f, a, c >2 < f a d' >2 < d g bf >8 r 2 < c f a >8 < c e a >8 < g, bf, d >4 < d g bf >2 r 8 < bf e' g' >4 < f bf d' >8 < f bf d' >8 < e a c' >8 < bf, d g >2 < c f a >8 < c e a >8 < c e g >2 < c e g >8 < e g c' >4 < g c' e' >8 r 4 < g c' e' >2 < e a c' >4 < bf e' g' >8 < c e a >4 < c e g >4 r 4 r 8 < g c' e' >4 r 4 r 8 < c f a >2 r 2 r 2 < a d' f' >8 < d g bf >2 < bf, d g >8 < g c' e' >8 < c f a >2 < bf, d g >2 < e a c' >4 < e g c' >2 r 2 < g, bf, d >2 < a, c f >8 < a d' f' >2 < bf, d g >4 < d f bf >4 < a, c e >2 < e g bf >4 < c e g >2 < c e a >8 < g, bf, d >8 r 2 < g, bf, d >8 r  < a, c f > < bf, d f > < d g bf > < c e a > < d f bf > < e g c' > < a d' f' > < f a d' > r  r  < d f bf > < a, c f > < e a c' > r  < bf, d g > < c e a > < a d' f' > < d f a > < g bf e' > < c f a > r  < a d' f' > < f, a, c > < a d' f' > r  r  < bf, d f >  }
 				 >>
		}
		>>

	\layout {
		 }

	\midi { }
	}