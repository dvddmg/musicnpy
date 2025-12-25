==========================
Logbook
==========================
--------------------------

Questa pagina è un piccolo diario di bordo che documenta lo sviluppo della libreria **musicnpy**.
Al suo interno si possono trovare informazioni riguardanti la sua struttura e le funzionalità da implementare in futuro.

Il progetto è stato iniziato durante il corso di *Sistemi e Linguaggi* presso il conservatorio *G. Verdi* di Milano con il maestro *Andrea Vigani*.

Structure
===========================

La libreria ha la seguente struttura:

.. code-block:: text

    musicnpy/
    ├── __init__.py
    ├── core.py
    ├── durs.py
    ├── pitch.py
    ├── velo.py
    └── topyly.py

Il modulo ``core`` è il cuore di tutta la libreria. Al momento fornisce un unica superclasse privata ``_Set`` da cui dipendono gli altri moduli.
Questa superclasse ha il compito gestire una lista di valori numerici con diversi scopi:

- Operazioni algebriche
- Trasformazioni numeriche
- Manipolazioni strutturali

Per approfondire: :doc:`core`.

Gli altri moduli contengono classi figlie di ``_Set``. Questa struttura peremette di ereditare tutte le funzioalità di base utilizzandole per i vari parametri musicali su cui sono specializzati i vari moduli (pitch, duration e velocity).

Il modulo ``topyly`` contine l'ultima versione della libreria **Pyly**.

Sintassi della libreria
---------------------------
Ci sono alcune cose da presentare rispetto al lavoro fatto: tutte le definizioni di classi e metodi sono documentati all'interno della libreria stessa con le docstring. 
Quest'ultime presentano le funzionalità e l'uso di ogni singola parte del codice. Inoltre, per generare la documentazione e facilitare la scrittura del codice, tutti gli argomento sono tipizzati con le *type hints* du Python. 
Questa cosa permette di avere degli snippet efficienti e precisi durante la scrittura; ha inoltre permesso di documentare tutta la libreria in maniera automatica grazie a Sphinx.

Le funzioni della libreria possono restituire nuovi oggetti o la propria istanza modificata. Questo aspetto permette di mantenere i dati originali inalterati e di creare catene di operazioni in maniera semplice ed efficiente.
I ``return self`` dei metodi permettono la concatenazione. Quando viene utilizzato un metodo invece che produce un nuovo output viene generato un nuovo oggetto oppure, in altri casi documentati, viene restituita una nuova lista.

Todo
===========================

- _Set:
    * implementare metodi di classe per `_Set`, generare patterns noti e randomici
    * aggiungere interpolazione
    * aggiungere normalizzazione
    * direzioni, contour

- _PSet:
    * conversioni: frequenze, midi e simboli
    * ottava, sopra, sotto o specifica
    * intervalli
    * gradi
    * classi figlie(Scale, Chord, Melody)
    * quantizzazione microtonale
    * quantizzazione a set di pitch

- _PDur:
    * gestione ritmi irregolari (_Set 2D)

- Classi ibride:
    * Arpeggio
    * Abbellimenti
    * ...

- topypy:
    * quarti e ottavi di tono