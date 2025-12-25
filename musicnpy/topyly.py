"""
NB: Questo modulo è una copia del file pyly.5.py
"""

import numpy as np
import os
# import sys
# import time
# import rtmidi
# from rtmidi.midiutil import open_midioutput
# from rtmidi.midiconstants import NOTE_OFF, NOTE_ON

# -------------------------------------------
# - COSTANTI
#   • PCHS (tuple)         = contiene i simboli delle altezze in formato lilypond
#   • DURS (tuple di dict) = {ratio:simbolo}
#   • IDURS (tule di dict) = {simbolo:ratio}
#   • VELS (tuple)         = contiene i simboli delle dinamiche in formato lilypond
#   • EXPR (Dict)          = contiene i simboli delle espressioni in formato lilypond
# -------------------------------------------
# - FUNZIONI:
#   • tonalita('Eb')               specifica tonalità con diesis o bemolli           
#   • mapPitch([60,64,67], 'd')    -1 = pausa, -2 = spazio (anche singolo int)
#   • mapDur([4, 8, [4,[3,2]]])    00 = valore precedente (anche singolo int)
#   • mapVel([127,64])             00 = senza simbolo (anche singolo int)
#   • mapExp([">","."])            00 = senza simbolo (anche singolo int)
#   • nDim([34,45,56])             riporta le dimensioni di una lista
#   • l_mod([34,45,56], 5)         target >= list, se < riporta la lista originale
#   • l_zero([34,00,56], 5)        target >= list, se < riporta la lista originale
#   • dflt(None)                   None, int, lista = crea lista o aggiunge 'zero' alla fine
#   • selmode([60,56],'zero'], 5)   genera lista di size target in base al modo specificato
#   • getmaxsize(note,dur,vel,exp) restituisce il size della lista più lunga
# -------------------------------------------
# - CLASSI:
#   • _Map(note=[60], dur=[4], vel=[64], exp=[">"])
#                       .note --> recupera lista di altezze
#                       .dur  --> recupera lista di durate
#                       .vel  --> recupera lista di velocities
#                       .exp  --> recupera lista di espressioni
#                       .max  --> size della lista più grande

#   • _Print(filename="score", format="pdf", version="2.24.4")
#                       .print_out --> stampa la stringa nel terminale
#                       .make_file --> genera tre files
#
#   • _Voice(note=60, dur=None, vel=None, exp=None,
#            filename="score", format="pdf", version="2.24.4")  --> ereditati dal _Print 
#                       .out       --> genera una stringa in output
#                       .print_out --> stampa la stringa nel terminale
#                       .make_file --> genera tre files)  
#
#   • Staff(voice=tuple di Voice,
#           key=None, t_sig=None, clef=None,
#           i_name=None, i_short=None, i_midi=None,
#           filename="score", format="pdf", version="2.24.4") --> ereditati dal _Print 
#                       .out       --> genera una stringa in output
#                       .print_out --> stampa la stringa nel terminale
#                       .make_file --> genera tre files
#   • Score(staff=tuple di Staff,
#           staff_size=None, indent=None, s_indent=None,
#           title=None, composer=None,
#           size="a4landscape", margins=(10,10,10,10),
#           filename="score", format="pdf", version="2.24.3") --> ereditati da _Print
#                       .out       --> genera una stringa in output
#                       .print_out --> stampa la stringa nel terminale
#                       .make_file --> genera tre files

# -------------------------------------------
# - COSTANTI

NOTE_DIESIS = ['c',  'cs', 'd',  'ds', 'e',  'f','fs', 'g',  'gs', 'a',  'as', 'b']
NOTE_BEMOLI = ['c',  'df', 'd',  'ef', 'e',  'f','gf', 'g',  'af', 'a',  'bf', 'b']

TONALITA_DIESIS = {'c',"g","d", "a", "e", "b", "fs","cs"}
TONALITA_BEMOLI = {"f","bf","ef","af","df","gf","cf"}

PCHS = {}
for n in range(128):
    diesis = NOTE_DIESIS[n % 12]
    bemoli = NOTE_BEMOLI [n % 12]
    octave = (n // 12) - 4
    if octave > 0:
        acc = "'" * octave
    elif octave < 0:
        acc = "," * (-octave)
    else:
        acc = ""
                # {61 : {'diesis':'cs', 'bemoli':'df'}}
    PCHS[n] = {'diesis': diesis + acc, 'bemoli': bemoli + acc} # riempie il dictionary

STEPS = ( '32',    '16',   '16.', '8',   # simboli lilypond
        '8~32',  '8.',   '8..',   '4',    
        '4~32',  '4~16', '4~16.', '4.',   
        '4.~32', '4..',  '4...', '2',                                                                
        '2~32',  '2~16', '2~16.', '2~8',  
        '2~8~32','2~8.', '2~8..', '2.',   
        '2.~32', '2.~16','2.~16.','2..',  
        '2..~32','2...', '2....', '1')
REGOLA = 1/32  * np.arange(1,33,1)                # tempi assoluti regolari
RATIOS = (1/1,3/2,5/4,6/4,7/4,9/8,11/8,13/8,15/8) # tempi assoluti regolari e irregolari
VALS = [REGOLA/i for i in RATIOS]
DURS = ({}, {},     {},      {},      {},      {},      {},       {},       {})
for n in range(len(VALS)):      # RATIO:'4'       
    for i in range(32):
        DURS[n][np.round(VALS[n][i], decimals=5)] = STEPS[i] 

IDURS = []
for i in range(len(DURS)):
    IDURS.append({v: k for k, v in DURS[i].items()})
IDURS = tuple(IDURS)

VELS = ('\\ppppp','\\pppp','\\ppp','\\pp','\\p','\\mp','\\mf','\\f','\\ff','\\fff','\\ffff','\\fffff')
EXPR = {
    # Articolazioni
    '>':   '->',     # accento
    '^':   '-^',     # marcato
    '!':   '-!',     # staccato secco
    '.':   '-.',     # staccato
    '_':   '-_',     # tenuto
    '-':   '--',     # legato
    'tie': '~',      # legatura di valore
   
    # Dinamica espressiva
    'expr': '\\espressivo',

    # Ornamenti e abbellimenti
    'tr':        '\\trill',      # trillo
    'm':         '\\mordent',    # mordente
    'cor':       '\\fermata',    # fermata
    'turn':      '\\turn',       # gruppetto
    'arpeggio':  '\\arpeggio',   # arpeggio

    # Glissando e hairpins
    'gliss': '\\glissando',  # glissando
    'cresc':     '\\<',          # inizio crescendo hairpin
    'dim':       '\\>',          # inizio diminuendo hairpin
    'end':       '\\!',          # chiusura hairpin

    # Respiri e arcate
    'breathe':   '\\breathe',    # segno di respiro
    'upbow':     '\\upbow',      # arcata in su
    'downbow':   '\\downbow',    # arcata in giù

    # Armonici
    'harmonic':       '\\harmonic',   # armonico naturale o artificiale
    'flageolet':      '\\flageolet',  # flageolet

    # Pizzicati come markup text
    'pizzicato':      '^\\markup { "pizz." }',  # pizzicato
    'bartokPizz':     '^\\snappizzicato',       # pizzicato Bartók

    00:          ''        # nessuna espressione
}

# -------------------------------------------
# - FUNZIONI:

def tonalita(key):
    """
    'diesis' per tonalità con #, 'bemoli' per tonalità con ♭.
    """
    if key is None:
        return 'diesis'

    if key in TONALITA_DIESIS:
        return 'diesis'
    else:
        return 'bemoli'
    
# a = tonalita('ef')
# print(a)

def mapPitch(a, key=None):
        '''
        Midinote --> Simboli Lilypond
        a   --> 0-127 -1 = pausa, -2 = spazio, 00 = valore precedente
        key --> tonalita (symbol - 'D')
        IN:  list (int) 
        OUT: list (string) 
        '''
        if type(a) is not list:
            a = [a]

        scegli = tonalita(key)      # Scegli tra 'diesis' e 'bemoli'
                        
        out = []
        for i in a:
            if type(i) is list:         # se accordo
                x = '< '
                for n in i:
                    if n == -1:
                        x += 'r '
                    elif n == -2:
                        x += 's '
                    else:
                        x += PCHS[n][scegli] + ' '
                out.append(x + '>')
            else:
                if i == -1:             # se pausa
                    out.append('r ')   
                elif i == -2:           # se spazio
                    out.append('s ')
                elif i == 00:           # se valore precedente
                    out.append('')     
                else:                   # se nota
                    out.append(PCHS[i][scegli]) 
        return out

#a = 63             # Singola nota
#a = mapPitch(a)
#print(a)

#a = [[60,64,67]]   # Singolo accordo
#a = mapPitch(a)
#print(a)

# a = [60,61,62]     # Sequenza monofonica
# a = mapPitch(a)
# print(a)

# a = [60, -1, 62, -2, 89] # Sequenza monofonica con pause e spazi vuoti
# a = mapPitch(a)
# print(a)

# a = [60, 00, 62, 00, 89] # Sequenza con ripetizion della stessa nota
# a = mapPitch(a)
# print(a)

# a = [64,[56,89]]    # Sequenza polifonica
# a = mapPitch(a)
# print(a)

#a = [62,[66, 69]]    # Tonalità con diesis
#a = mapPitch(a,k)
#print(a)
#k = 'd'

# a = [63,[67, 70]]    # Tonalità con bemoli
# k = 'ef'
# a = mapPitch(a,k)
# print(a)

def mapDur(a):          
        '''
        Durate --> Simboli Lilypond
        00 = valore precedente
        IN:  list (int/list 2D) o int
        OUT: list (string) 
        '''
        if type(a) is not list:
            a = [a]                 # Casting
        out = []                               
        for i in a:
            if type(i) == list:     # se irregolare o puntato
                irr  = []
                sudd = []  
                if sum(i[1]) in (4,8,16,32):
                    for d in i[1]:   
                        out.append(DURS[0][round((1/i[0] / sum(i[1])) * d,5)]) 
                elif sum(i[1]) in (3,3):
                    irr.append('\\tuplet 3/2')
                    for d in i[1]:
                        sudd.append(DURS[1][round((1/i[0] / sum(i[1])) * d,5)])   
                    irr.append(sudd)
                    out.append(irr)
                elif sum(i[1]) in (5,10):
                    irr.append('\\tuplet 5/4')  
                    for d in i[1]:
                        sudd.append(DURS[2][round((1/i[0] / sum(i[1])) * d,5)]) 
                    irr.append(sudd)
                    out.append(irr)
                elif sum(i[1]) in (6,12):
                    irr.append('\\tuplet 6/4') 
                    for d in i[1]:
                        sudd.append(DURS[3][round((1/i[0] / sum(i[1])) * d,5)]) 
                    irr.append(sudd)
                    out.append(irr)
                elif sum(i[1]) in (7,14):
                    irr.append('\\tuplet 7/4')
                    for d in i[1]:   
                        sudd.append(DURS[4][round((1/i[0] / sum(i[1])) * d,5)])
                    irr.append(sudd)
                    out.append(irr)
                elif sum(i[1]) in (9,12):
                    irr.append('\\tuplet 9/8')
                    for d in i[1]:   
                        sudd.append(DURS[5][round((1/i[0] / sum(i[1])) * d,5)])
                    irr.append(sudd)
                    out.append(irr)
                elif sum(i[1]) in (11,22):
                    irr.append('\\tuplet 11/8')
                    for d in i[1]:   
                         sudd.append(DURS[6][round((1/i[0] / sum(i[1])) * d,5)])
                    irr.append(sudd)
                    out.append(irr)
                elif sum(i[1]) in (13,26):
                    irr.append('\\tuplet 13/8')
                    for d in i[1]:   
                        sudd.append(DURS[7][round((1/i[0] / sum(i[1])) * d,5)])
                    irr.append(sudd)
                    out.append(irr)
                elif sum(i[1]) in (15,30):
                    irr.append('\\tuplet 15/8')
                    for d in i[1]:   
                        sudd.append(DURS[8][round((1/i[0] / sum(i[1])) * d,5)])
                    irr.append(sudd)
                    out.append(irr)
            else:
                if i == 00:                  # se 00 valore precedente 
                    out.append('')         
                else:
                    out.append(DURS[0][1/i]) # se regolare  
        return out 

##a = mapDur(a)
#a = 4                # Singola durata
#print(a)

#a = [4,8,8]          # Sequenza di durate
#a = mapDur(a)
#print(a)

#a = [4,[4,[7,1,3]]]    # Ritmi puntati o irregolari
#a = mapDur(a)
#print(a)

def mapVel(a):
        ''' 
        Velocities --> Simboli Lilypond
        00 = valore precedente
        IN:  list (int)
        OUT: list (string) 
        '''
        if type(a) is not list:
            a = [a]                     # Casting
        out = []       
        for i in a:                
            if i > 0:              
                if 1 <= i <= 9:         
                    out.append(VELS[0])  # ppppp
                elif 10 <= i <= 19:
                    out.append(VELS[1])  # pppp
                elif 20 <= i <= 29:
                    out.append(VELS[2])  # ppp
                elif 30 <= i <= 39:
                    out.append(VELS[3])  # pp
                elif 40 <= i <= 49:
                    out.append(VELS[4])  # p
                elif 50 <= i <= 59:
                    out.append(VELS[5])  # mp
                elif 60 <= i <= 69:
                    out.append(VELS[6])  # mf
                elif 70 <= i <= 79:
                    out.append(VELS[7])  # f
                elif 80 <= i <= 89:
                    out.append(VELS[8])  # ff
                elif 90 <= i <= 99:
                    out.append(VELS[9])  # fff
                elif 100 <= i <= 109:
                    out.append(VELS[10]) # ffff
                else: 
                    out.append(VELS[11]) # fffff
            else:
                out.append('')           # 00 valore precedente 
        return out

# a = 60             # Singola velocity
# a = mapVel(a)
# print(a)

# a = [60,81,102]     # Sequenza di velocities
# a = mapVel(a)
# print(a)

# a = [60,00,81,00,102]     # Sequenza di velocities alternate
# a = mapVel(a)
# print(a)

def mapExp(a):   
        ''' 
        Simboli --> Simboli Lilypond
        00 = valore precedente
        IN:  list (string)
        OUT: list (string) 
        '''
        if type(a) is not list:
            a = [a]             # Casting
        out = []                          
        for i in a:                   
            out.append(EXPR[i])                    
        return out 

# a = 'tr'                        # Singola espressione
# a = mapExp(a)
# print(a)

#a = mapExp(a)
#a = ['.','>', 'gliss', 'tie']   # Sequenza di espressioni
#print(a)

# a = ['.','>', 00, '!']          # Sequenza di espressioni con buchi
# a = mapExp(a)
# print(a)

def nDim(a):
    '''Riporta le dimensioni di una lista:
    1D = Tutto
    2D = Solo accordi (pitches)
    3D = Solo ritmi irregolari o puntati
    '''
    if not isinstance(a, list):
        return 0
    elif not a:
        return 1
    else:
        return 1 + max(nDim(item) for item in a)   # Ricorsione

# d = [23,34,45,[34,[45,56]]]
# e = nDim(d)
# print(e)

def l_mod(lista, target):
    '''
    Genera una lista di n elementi (target) ripetendo la lista originale con operatore modulo.
    Se la lista contiene elementi irregolari (liste 2D), li espande correttamente.
    '''
    nl = []
    count = 0
    if nDim(lista) == 3:                 # Se lista 3D (contiene ritmi irregolari)
        idx = 0
        while count < target:            # Fino a quando count < target 
            el = lista[idx % len(lista)] # prende l'elemento corrente
            if type(el) == list:         # se irregolare (2D)
                sudd = []
                for i in el[1]:          # per ogni suddivisione
                    if count < target:
                        sudd.append(i)   # aggiunge la suddivisione 
                        count += 1       # aggiorna il count
                    else:
                        break            # esce dal ciclo se count >= target 
                nl.append([el[0], sudd])
            else:                        # altrimenti aggiorna di 1 
                nl.append(el)
                count += 1
            idx += 1
    else:                                # Se lista 1D o 2D (note o accordi)
        for i in range(target):
            nl.append(lista[i % len(lista)])
    return nl

#a = [60,64,67]          # Sequenza monofonica pitches
#a = l_mod(a, 10)
#print(a)

#a = [60,[64,67],89,90]        # Sequenza polifonica pitches
#print(a)
#a = l_mod(a, 10)

# a = [4,8,8,2]           # Sequenza ritmica regolare
# a = l_mod(a, 10)
# print(a)

#a = [[4,[1,1,2,3]],8,8,[8,[1,1,1]],32] # Sequenza ritmica irregolare
#print(a)
#a = l_mod(a, 12)

def l_zero(lista, target):
    '''
    Genera una lista di n elementi (target) sostituendo gli zeri (00) con ''.
    Se la lista è più corta di target, aggiunge '' alla fine fino a raggiungere target.
    '''
    nl = []
    idx = 0
    for i in range(len(lista)):
        el = lista[i]
        idx += 1
        if nDim(el) == 2:         # Se lista 3D (contiene ritmi irregolari)
            idx += len(el[1])
            idx -= 1
            if el == 00:
                 nl.append('')
            else:
                nl.append(el)
        else:
            if el == 00:
                 nl.append('')
            else:
                nl.append(el)
    for i in range(target-idx):
        nl.append('')
    return nl

# a = [69,67,68]      # Sequenza monofonica pitches
# a = l_zero(a,5)
# print(a)

# a = [69,[67,68]]    # Sequenza polifonica pitches
# a = l_zero(a,5)
# print(a)

# a = [4,8,8]  # Sequenza ritmi regolari
# a = l_zero(a,5)
# print(a)

#a = [16,8,16,[4,[1,2,4,5]],4, [4,[1,1,1]]] # Sequenza ritmi irregolari
#print(a)
#a = l_zero(a,19)

def dflt(a):
    '''
    Genera array di default e aggiunge uno zeropad se aromento è:
    • None
    • int
    • lista
    '''
    if a is None:                      # SE non esiste
        out = [0,'zero']                 # ---> mette default
    elif type(a) is not list:          # SE è int singolo
        out = [a,'zero']                 # --> crea una lista
    elif a[-1] != 'mod' and a[-1] != 'zero': # SE non specifica il modo
        a.append('zero')                     # --> lo mette di default
        out = a
    else:
        out = a                         # altrimenti lo assegna
    return out
   
# a = None       # Se non specifichiamo argomento
# a = dflt(a)   
# print(a)

# a = 60           # Se specifichiamo singolo int
# a = dflt(a)   
# print(a)

# a = [[60,64,67]]  # Se NON specifichiamo 'zero' or 'mod' 
# a = dflt(a)   
# print(a)

# a = [[60,64,67], 'mod']  # Se specifichiamo tutto 
# a = dflt(a)   
# print(a)

def selmode(lista, max):
    '''
    Genera liste di diversa lunghezza in base al modo specificato
    lista = [60, 'zero']
    max   = target size 
    '''
    if lista[1] == 'mod':             # SE mod
        out = l_mod(lista[0], max)
    else:                             # SE zero
        out = l_zero(lista[0], max) 
    return out

# a = [[60,64,67], 'mod']  # Operatore modulo 
# a = selmode(a, 10)   
# print(a)

# a = [[60,64,67], 'zero']  # zeropad
# a = selmode(a, 10)   
# print(a)

def getmaxsize(note,dur,vel,exp):
    '''Trova il size della lista più lunga'''
    idx = 0                      # conteggio esatto elementi in durate
    for i in dur:
        if type(i) == list:                      # se irregolare
            idx = idx + len(i[1])
        else: idx += 1                           # se regolare
    return max(len(note),idx,len(vel),len(exp))  # trova il size max

# -------------------------------------------
# - CLASSI:

class _Map:
    '''
    Esegue il mapping.
    Accetta liste di lunghezza diversa in ingresso.
    Genera liste di lunghezza uguale (l_map oppure l_zero)
    e le assegna a variabili d'istanza richiamate nelle classi figlie
    IN:  • pchs = list (int/list 2D) oppure int
         • durs = list (int/list 2D) oppure int
         • vels = list (int) oppure int
         • expr = list (string) oppure int
    '''   
    def __init__(self, note=60,dur=None,vel=None,exp=None,key=None):

        self.note = dflt(note)  # Assegna le variabili locali e genera eventuali default (dflt())
        self.dur  = dflt(dur)
        self.vel  = dflt(vel)
        self.exp  = dflt(exp)
        self.key  = key

        self.note = [self.note[0:-1], self.note[-1]]    # [[seq], tipo] 
        self.dur  = [self.dur[0:-1], self.dur[-1]]
        self.vel  = [self.vel[0:-1], self.vel[-1]]
        self.exp  = [self.exp[0:-1], self.exp[-1]]

        self.note[0] = mapPitch(self.note[0],self.key)  # mapping con liste senza 'mod o 'zero'
        self.dur[0]  = mapDur(self.dur[0]) 
        self.vel[0]  = mapVel(self.vel[0]) 
        self.exp[0]  = mapExp(self.exp[0]) 

        self.max  = getmaxsize(self.note[0],self.dur[0],self.vel[0],self.exp[0]) # trova il size max delle liste
                                                                                 # per normalizzazione
        self.note = selmode(self.note, self.max) # normalizza la lunghezza delle liste
        self.dur  = selmode(self.dur, self.max)  # in due modalità 'mod' oppure 'zero'
        self.vel  = selmode(self.vel, self.max)
        self.exp  = selmode(self.exp, self.max)
 
#p = [60,45,56,[67,78,89],67,56,67] # Sequenza monodica
#v = 89
#d = [4,  [4,[1,1,1]],4,4,8,8,8,'zero']
#e = ['.','>','mod']

#a = _Map(p, d, v, e, 'd')

#print(a.note)
#print(a.dur)
#print(a.vel)
#print(a.exp)

class _Print:
    '''
    Salva un file lilypond (.ly) e lo compila generando:
        - un file grafico
        - un file midi
    IN: • filename (string)
        • format (string [pdf, png, pngalpha, svg, ps])
        • version (string)             
    '''
    def __init__(self,
                 filename="score", format="pdf",
                 version="2.24.4"
                ):

        self.filename  = filename
        self.format    = format
        self.version   = version

    @property
    def print_out(self):
        '''
        Restituisce una stringa con il codice lilypond
        self.outstring lo prende dalle sottoclassi
        '''
        self.outo = f"\n\\version \"{self.version}\"\n\\language \"english\"\n\n{self.outstring}"
        print(self.outo)
    
    @property
    def make_file(self):
        '''
        Genera tre files: .ly .format e .midi
        '''
        self.outo = f"\n\\version \"{self.version}\"\n\\language \"english\"\n{self.outstring}"
        f = open(self.filename + ".ly", "w")  # crea un file di testo...
        f.write(self.outo)                    # lo scrive...
        f.close()                             # lo chiude in python

        cmd = f"lilypond -dresolution=300 -dpixmap-format=png16m --format={self.format} --output={self.filename} {self.filename}.ly"
        os.system(cmd)   

class _Voice(_Print):
    '''
    Costruisce una voce musicale in formato lilypond
    Le liste possono essere di lunghezza differente
    IN: • midinote ([60])          oppure int
        • durate ([4, [4,[3,1]]])  oppure int
        • velocity ([64])          oppure int 
        • espressioni  (['>''])    oppure int
    OUT: un'espressione musicale di lilypond (stringa)
    '''
    def __init__(self,
                 note=60,dur=None,vel=None,exp=None,key=None,
                 filename="score", format="pdf", version="2.24.3"
                 ):
        super().__init__(filename,format,version)

        ins = _Map(note,dur,vel,exp,key)    # Crea liste della stessa lunghezza
        self.note = ins.note
        self.dur  = ins.dur 
        self.vel  = ins.vel 
        self.exp  = ins.exp 
        self.music   = ''
        self.id      = -1
        
        for i in self.dur:
            if type(i)==list:
                self.irr = ''
                self.irr = self.irr + i[0] + ' { '
                for n in i[1]:
                    self.id += 1 
                    self.irr = self.irr + self.note[self.id] + n + self.vel[self.id] + self.exp[self.id] + ' '             
                self.irr = self.irr + '} '
                self.music = self.music + self.irr                            
            else:                                  
                self.id += 1                            
                self.music = self.music + self.note[self.id] + i + self.vel[self.id] + self.exp[self.id] + ' '     
                  
        self.outstring = f"{{ {self.music} }}"
        
    @property
    def out(self):
        return self.outstring
    
#p = [60,64,67,72,67,76,67,69]      # Sequenza monofonica ritmo regolare
#d = [ 8,16,16, 4, 'mod']
#v = [60,80,00,90, 'zero']
#e = ['.','.','.',00,'>','zero']

#a = _Voice(p,d,v,e,'acci').make_file

#p = [60,64,67,[64,72,75],67,76,67,69,71,'mod'] # Sequenza polifonica ritmo regolare
#d = [ 8,16,16, 4, 16,16,16,16,16,16,8,'mod']
#v = [60,80,00,90, 'zero']
#e = ['.','.','.',00,'>','zero']

#a = _Voice(p,d,v,e).make_file

#p = [60, 64, 67,     72,67,76, 67, 69, 71]      # Sequenza monofonica ritmo irregolare
#d = [ 8, 16, 16, [4,[2, 1, 2]], 'mod']
#v = [60,     00,00,90,'zero']
#e = ['cresc',00,00,'dim',00,00,00,'end']

#a = _Voice(p,d,v,e).make_file

#p = [60, 64, 67,     [72,67,76], 67, -1, 71,82,78,60,61] # Sequenza polifonica ritmo irregolare
#v = [60,     00,00,90,00,00,00,00,54,'zero']
#d = [ 8, 16, 16, [4,[1, 3,3, 3,4]], 'mod']
#e = ['cresc',00,00,'dim',00,00,00,00,00,'>','end']

#a = _Voice(p,d,v,e).make_file

# ============================================================
# PER OGNI PARAMETRO:
# Se 1 sola voce per staff ---> lista
# Se più voci per staff    ---> tuple di liste

class Staff(_Print):
    '''
    Costruisce un rigo musicale in formato lilypond
    Le liste possono essere di lunghezza differente
    IN: • midinote ([60])          oppure int
        • durate ([4, [4,[3,1]]])  oppure int
        • velocity ([64])          oppure int 
        • espressioni  (['>''])    oppure int
        • tonalità ('C')
        • tempo ('3/4')
        • chiave ('bass')
        • nome strumento ('Violino')
        • nome abbreviato ('Vl')
        • nome MIDI ('violino')
    OUT: un'espressione musicale di lilypond (stringa)
    '''
    def __init__(self,
                 note=60,dur=None,vel=None,exp=None,
                 key=None,t_sig=None,clef=None,
                 i_name=None,i_short=None,i_midi=None,
                 filename="score", format="pdf", version="2.24.3"
                 ):
        super().__init__(filename,format,version)

        self.voice = []
        if type(note) == tuple: 

            for i, _ in enumerate(note):
                voicedur = None if dur is None else dur[i]
                voicevel = None if vel is None else vel[i]
                voiceexp = None if exp is None else exp[i]

                a = _Voice(note[i], voicedur, voicevel, voiceexp, key)
                self.voice.append(a.out)
        else:
            self.voice.append(_Voice(note,dur,vel,exp,key).out)

        self.multivoice = ""
        self.items = len(self.voice)
        self.cnt = 0
        for v in self.voice:
            if self.items > 1 and self.cnt < self.items-1:
                self.multivoice += f" \t\t\t\t {v} \n\t\t\t\t   \\\\\n"
                self.vseq = f"\t <<\n {self.multivoice} \t\t\t\t >>"
            elif self.cnt == self.items-1:
                self.multivoice += f" \t\t\t\t {v}\n"
                self.vseq = f"\t <<\n {self.multivoice} \t\t\t\t >>"
            else:
                self.multivoice = f"\t {v}"
                self.vseq = self.multivoice
            self.cnt += 1        
        

        self.clef    = f"\n\t\t\t\t  \\clef {clef}" if clef   else ""
        self.i_name  = f"\n\t\t\t\t  instrumentName=\"{i_name}\"" if i_name else ""
        self.i_short = f"\n\t\t\t\t  shortInstrumentName=\"{i_short}\"" if i_short else ""
        self.i_midi  = f"\n\t\t\t\t  midiInstrument=\"{i_midi}\"" if i_midi else '\n\t\t\t\t  midiInstrument="acoustic grand"'

        
        self.outstring = (
            
            "\t\t\\new Staff \\with {" +
            f"{self.i_name}{self.i_short}{self.i_midi}{self.clef}\n" +
            "\t\t\t\t  } " +
            
            "{\n" +
            (f"\t\t\t\t  \\key {key} \\major\n"                       if key   else "") +
            (f"\t\t\t\t  \\numericTimeSignature\n"                    if t_sig else "") +
            (f"\t\t\t\t  \\time {t_sig}\n"                            if t_sig else "") +
            f"\t\t\t{self.vseq}\n" +
            "\t\t}"
        )
        

    @property
    def out(self):
        return self.outstring
        
# p = [61,64,67,73,67,76,67,69,76,66,64]      # Sequenza monofonica ritmo regolare
# d = [ 8,16,16, 8, 'mod']
# v = [60, 'zero']
# e = ['.','.','.',00,'>','zero']

# a = Staff(p,d,v,e,key='d',t_sig='3/4',clef='G',i_name='Ciccio').make_file

# p = [61,[64,67],73,[67,76],67,[69,76,66],64,60,'mod']  # Sequenza polifonica ritmo regolare
# d = [ 8,16,16, 8, 'mod']
# v = [60,80,00,90, 'zero']
# e = ['.','.','.',00,'>','zero']

# a = Staff(p,d,v,e,key='e',t_sig='3/8',clef='G',i_name='Ciccio').make_file

# p = [61,64,67,73,67,76,67,69,76,66,64]      # Sequenza monofonica ritmo irregolare
# d = [ [8,[1,1,1]],8,[8,[2,1,2]], 'mod']
# v = [60,80,00,90, 'zero']
# e = ['.','.','.',00,'>','zero']

# a = Staff(p,d,v,e,key='bf',t_sig='5/8',clef='C',i_name='Ciccio').make_file

# p = [61,[64,67],73,[67,76],67,[69,76,66],64,60,87,76,65,'mod']  # Sequenza polifonica ritmo itregolare
# d = [ [8,[1,1,1]],8,[8,[2,1,2]], 'mod']
# v = [60,80,00,90, 'zero']
# e = ['.','.','.',00,'>','zero']

# a = Staff(p,d,v,e,key='e',t_sig='2/4',clef='G',i_name='Ciccio').make_file

# Sequenza polifonica ritmo irregolare

# pa = [61,[64,67],73,[67,76],67,[69,76,66],64,60,87,76,65,'mod']  
# da = [ [8,[1,1,1]],8,[8,[2,1,2]], 'mod']
# va = [60,80,00,90, 'zero']
# ea = ['.','.','.',00,'>','zero']

# pb = [56,54,52]
# db = [8,  8, 8]
# vb = None
# eb = None

# p = (pa,pb)
# d = (da,db)
# v = (va,vb)
# e = (ea,eb)

# a = Staff(p,d,v,e,key='e',t_sig='2/4',clef='G',i_name='Ciccio').make_file


class Score(_Print):
    '''
        Definisce le caratteristiche della partitura. 
        Formattando gli outputs delle classi precedenti. 
        Di default crea uno StaffGroup.
        IN: • staff (tuple di output di una o più istane di Staff)
            • staff_size (in mm)
            • indent (rientro in mm)
            • s_indent (short indent in mm)
            • titolo (title - stringa)
            • compositore (composer - stringa)
            • size pagina (size - stringa)
              - formati standard: https://lilypond.org/doc/v2.25/Documentation/notation/predefined-paper-sizes
              - se tuple con due int -> custom largh/alt in pixels
            • margini (margins - tuple in mm)
    '''
    def __init__(self, 
                 staff="\n\t\t{c' d' e' f'}",
                 staff_size=None, indent=None, s_indent=None,
                 title=None, composer=None,
                 size="a4landscape", margins=(10,10,10,10),
                 filename="score", format="pdf", version="2.24.3"    # ereditati da _Print
                ):
        super().__init__(filename,format,version)

        if type(staff) == tuple:
            self.staff = staff
        else: 
            self.staff = [staff]

        self.staff_size = f"\n\t#(layout-set-staff-size {staff_size})" if staff_size is not None else ""
        self.indent     = f"\n\tindent = {indent}" if indent is not None else ""
        self.s_indent   = f"\n\tshort-indent = {s_indent}" if s_indent is not None else ""
        self.layout     = f"\n\t\\layout {{{self.staff_size}{self.indent}{self.s_indent}\n\t\t }}"

        self.title      = "\n\ttitle=\""+title+"\"" if title is not None else "" 
        self.composer   = "\n\tcomposer=\""+composer+"\"" if composer is not None else ""
        if type(size) is tuple:          
            self.custom = f"#(set! paper-alist (cons \'(\"mio formato\" . (cons (* {size[0]} mm) (* {size[1]} mm))) paper-alist) )"
            self.size   = "\n\t#(set-paper-size \"mio formato\")"
        else: self.custom, self.size = "", f"\n\t#(set-paper-size \"{size}\")"
        self.margins  = f"\n\ttop-margin={margins[0]}\n\tbottom-margin={margins[1]}\n\tleft-margin={margins[2]}\n\tright-margin={margins[3]}" 

        self.page = f'''\\header {{{self.title}{self.composer}\n\ttagline=\"\"\n\t}}
        {self.custom}\n\\paper {{{self.size}{self.margins}\n\t}}'''

        self.multistaff = ""
        for i in self.staff:
            self.multistaff = self.multistaff + i + "\n"
        self.outstring = f'''{self.page}\n\n\\score {{\n\t\\new StaffGroup\n\t\t<<\n{self.multistaff}\t\t>>\n{self.layout}\n\n\t\\midi {{ }}\n\t}}'''

    def sei_libero(self):
        '''
        Nasconde indicazione di tempo e linee di battuta.
        '''
        hide_layout = (
            "\n\t\\layout {"
            "\n\t  \\context {"
            "\n\t    \\Staff"
            "\n\t    \\remove \"Time_signature_engraver\""
            "\n\t    \\remove \"Bar_engraver\""
            "\n\t  }"
            "\n\t}" 
        )
        # Sostituisci l'impostazione layout attuale
        self.outstring = self.outstring.replace(self.layout, hide_layout)
        self.layout = hide_layout
        return self


# p = [61,64,67,73,-1,76,67,-1,76,66,64]      # Sequenza monofonica ritmo regolare
# d = [ 8,16,16, 8, 'mod']
# v = [60,80,00,90, 'zero']
# e = ['.','.','.',00,'>','zero']

# a = Staff(p,d,v,e,key='cf',t_sig='3/8',clef='C',i_name='Ciccio').out

# r = [61,[64,67],73,[67,76],67,[69,76,66],64,60,'mod']  # Sequenza polifonica ritmo regolare
# u = [ 8,16,16, 8, 'mod']
# t = [60,80,00,90, 'zero']
# n = ['.','.','.',00,'>','zero']

# b = Staff(r,u,t,n,key='e',t_sig='3/8',clef='G',i_name='Pasticcio').out

# staff = (a, b)
# a = Score(staff,title='ammazza', composer='stika',staff_size=[2,3]).make_file

# p = [61,64,67,73,67,76,67,69,76,66,64]      # Sequenza monofonica ritmo irregolare
# d = [ [8,[1,1,1]],8,[8,[2,1,2]], 'mod']
# v = [60,80,00,90, 'zero']
# e = ['.','.','.',00,'>','zero']

# a = Staff(p,d,v,e,key='bf',t_sig='5/8',clef='C',i_name='Ciccio').make_file

# p = [61,[64,67],73,[67,76],67,[69,76,66],64,60,87,76,65,'mod']  # Sequenza polifonica ritmo itregolare
# d = [ [8,[1,1,1]],8,[8,[2,1,2]], 'mod']
# v = [60,80,00,90, 'zero']
# e = ['.','.','.',00,'>','zero']

# a = Staff(p,d,v,e,key='e',t_sig='2/4',clef='G',i_name='Ciccio').make_file

# Sequenza polifonica ritmo itregolare

# pa = [61,[64,67],73,[67,76],67,[69,76,66],64,60,87,76,65,'mod']  
# da = [ [8,[1,1,1]],8,[8,[2,1,2]], 'mod']
# va = [60,80,00,90, 'zero']
# ea = ['.','.','.',00,'>','zero']

# pb = [56,54,52]
# db = [8,  8, 8]
# vb = None
# eb = None

# p = (pa,pb)
# d = (da,db)
# v = (va,vb)
# e = (ea,eb)

# a = Staff(p,d,v,e,key='e',t_sig='2/4',clef='G',i_name='Ciccio').make_file
