
\version "2.24.3"
\language "english"
\header {
	tagline=""
	}
        #(set! paper-alist (cons '("mio formato" . (cons (* 250 mm) (* 65 mm))) paper-alist) )
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
  				 { < a c' as' b' f'' fs'' as'' b'' d''' ds''' f''' fs''' gs''' gs''' as''' b''' c'''' cs'''' d'''' ds'''' e'''' e'''' f'''' fs'''' g'''' g'''' gs'''' gs'''' a'''' a'''' as'''' b'''' >2 a16 c'16 as'16 b'16 f''16 fs''16 as''16 b''16 d'''16 ds'''16 f'''16 fs'''16 gs'''16 gs'''16 as'''16 b'''16 c''''16 cs''''16 d''''16 ds''''16 e''''16 e''''16 f''''16 fs''''16 g''''16 g''''16 gs''''16 gs''''16 a''''16 a''''16 as''''16 b''''16  }
 				 >>
		}
		>>

	\layout {
	  \context {
	    \Staff
	    \remove "Time_signature_engraver"
	    \remove "Bar_engraver"
	  }
	}

	\midi { }
	}