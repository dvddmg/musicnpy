******************************
Introduzione
******************************

Questa libreria è un progetto in sviluppo, alcune parti sono ancora in fase di costruzione.
Il progetto è stato iniziato durante il corso di *Sistemi e Linguaggi* presso il conservatorio *G. Verdi* di Milano con il maestro *Andrea Vigani*.

Struttura
===========================

La libreria ha la seguente struttura:

.. code-block:: text

    musicnpy/
    ├── __init__.py
    ├── collections.py
    ├── core.py
    ├── data.py
    ├── durs.py
    ├── pitch.py
    ├── topyly.py
    └── velo.py

Moduli
===========================

- **core** 
    E' il cuore della libreria per la composizione assistita. Contiene la classe ``_Set`` che è la classe madre per tutte le classi figlie che gestiscono altezze, durate e velocity.
- **collections** 
    Fornisce dei contenitori in cui inserire i dati musicali completi come rappresentazione più ampia, tipo un pattern con altezze, durate e velocity.
- **data** 
    Contiene i modelli musicali di base comuni da utilizzare come punto di partenza per la creazione di nuovi algoritmi.
- **pitch** 
    Tutte le classi e funzioni per la gestione delle altezze musicali.
- **durs** 
    Tutte le classi e funzioni per la gestione delle durate musicali.
- **velo** 
    Tutte le classi e funzioni per la gestione delle velocity musicali.
- **topyly**
    E' il modulo della libreria che permette di creare un output dagli algoritmi creati con i moduli precedentei. Gli output possono essere file lylipond, MIDI, grafici o sonori grazie e FluidSynth.

Note
===========================

La libreria è completa di docstring per ogni funzione e classe. Questo aspette permette di collegare durante la scrittura del condice la documentazione fatta. Inoltre questa documentazione è stata generata partendo dalle stesse docstring.
