
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
  				 { r 2 bf'2 a'4 g'4 r 8 r 4 r 4 r 8 r 8 g'8 bf'4 bf'2 bf'4 d''2 g'2 g'4 g'8 g'8 r 4 bf'8 d''4 c''4 a'4 f'8 r 4 r 2 r 8 d''2 e''4 r 4 r 8 d''2 r 2 f'4 d''4 g'8 g'8 r 8 c''4 g'2 r 8 g'8 c''4 a'4 c''8 c''4 g'8 c''8 d''2 c''4 r 8 r 4 g'4 e''8 r 8 d''2 d''2 bf'2 c''4 c''4 bf'4 r 8 bf'4 r 2 f'2 g'4 bf'4 r 8 f'4 a'4 r 8 e''4 c''4 d''8 r 4 a'4 r 8 c''8 r 8 a'8 r 8 r 2 d''4 e''8 d''8 bf'4 c''2 a'8 r 2 e''4 c''2 f'8 c''2 f'4 bf'2 g'8 r 4 d''2 g'8 e''8 a'2 bf'4 g'4 a'8 c''8 e''8 a'8 r 2 c''4 bf'4 g'8 e''4 a'2 bf'2 a'4 g'2 r 4 e''4 d''8 a'4 bf'4 a'8 e''2 c''2 d''8 r 8 d''2 e''4 e''4 r 8 e''2 d''8 f'8 r 4 e''4 d''8 d''4 c''2 d''2 a'4 e''4 c''4 g'4 a'2 e''2 c''8 c''2 g'4 bf'4 r 8 c''2 r 8 r 8 e''8 r 8 e''8 f'8 g'8 r 8 r 8 d''8 d''8 r 8 f'8 r 8 f'8 d''8 r 8 bf'8 bf'8 a'8 r 8 e''8 g'8 r 8 r 8 f'8 r 8 g'8 a'8 f'8 f'8 a'8 e''8 g'8 d''8 e''8 g'8 g'8 a'8 d''8 f'8 r 8 d''8 e''8 bf'8 a'8 c''8 e''8 e''8  }
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
  				 { r 2 < f bf d' >2 < e a c' >4 < d g bf >4 r 8 r 4 r 4 r 8 r 8 < d g bf >8 < bf, d f >4 < d f bf >2 < d f bf >4 < d f a >2 < bf, d g >2 < bf, d g >4 < g, bf, d >8 < g, bf, d >8 r 4 < f bf d' >8 < f a d' >4 < g c' e' >4 < a, c e >4 < a, c f >8 r 4 r 2 r 8 < d f a >2 < e g bf >4 r 4 r 8 < d f a >2 r 2 < c f a >4 < f a d' >4 < d g bf >8 < bf, d g >8 r 8 < e g c' >4 < bf, d g >2 r 8 < bf, d g >8 < e g c' >4 < a, c e >4 < e g c' >8 < g c' e' >4 < g, bf, d >8 < e g c' >8 < d f a >2 < e g c' >4 r 8 r 4 < g, bf, d >4 < bf e' g' >8 r 8 < d f a >2 < f a d' >2 < f bf d' >2 < c e g >4 < g c' e' >4 < bf, d f >4 r 8 < d f bf >4 r 2 < a, c f >2 < d g bf >4 < d f bf >4 r 8 < c f a >4 < e a c' >4 r 8 < bf e' g' >4 < c e g >4 < d f a >8 r 4 < c e a >4 r 8 < e g c' >8 r 8 < c e a >8 r 8 r 2 < f a d' >4 < g bf e' >8 < f a d' >8 < bf, d f >4 < c e g >2 < e a c' >8 r 2 < g bf e' >4 < e g c' >2 < c f a >8 < g c' e' >2 < f, a, c >4 < f bf d' >2 < bf, d g >8 r 4 < f a d' >2 < bf, d g >8 < bf e' g' >8 < a, c e >2 < d f bf >4 < bf, d g >4 < e a c' >8 < g c' e' >8 < e g bf >8 < c e a >8 r 2 < g c' e' >4 < d f bf >4 < d g bf >8 < bf e' g' >4 < e a c' >2 < f bf d' >2 < e a c' >4 < g, bf, d >2 r 4 < e g bf >4 < d f a >8 < a, c e >4 < f bf d' >4 < e a c' >8 < g bf e' >2 < g c' e' >2 < d f a >8 r 8 < d f a >2 < g bf e' >4 < g bf e' >4 r 8 < e g bf >2 < d f a >8 < c f a >8 r 4 < bf e' g' >4 < a d' f' >8 < f a d' >4 < g c' e' >2 < f a d' >2 < e a c' >4 < bf e' g' >4 < e g c' >4 < g, bf, d >4 < a, c e >2 < bf e' g' >2 < e g c' >8 < g c' e' >2 < d g bf >4 < d f bf >4 r 8 < e g c' >2 r 8 r 8 < g bf e' >8 r 8 < g bf e' >8 < c f a >8 < bf, d g >8 r 8 r 8 < f a d' >8 < d f a >8 r 8 < f, a, c >8 r 8 < a, c f >8 < f a d' >8 r 8 < d f bf >8 < d f bf >8 < a, c e >8 r 8 < bf e' g' >8 < d g bf >8 r 8 r 8 < a, c f >8 r 8 < d g bf >8 < e a c' >8 < c f a >8 < f, a, c >8 < a, c e >8 < g bf e' >8 < bf, d g >8 < a d' f' >8 < e g bf >8 < d g bf >8 < bf, d g >8 < c e a >8 < a d' f' >8 < f, a, c >8 r 8 < a d' f' >8 < bf e' g' >8 < d f bf >8 < e a c' >8 < e g c' >8 < g bf e' >8 < g bf e' >8  }
 				 >>
		}
		>>

	\layout {
		 }

	\midi { }
	}