import numpy as np
import os
import time as t
import fluidsynth
import threading

# path = os.path.abspath('./pycac')
# sys.path.insert(0, path)

# import Scale from pycac.pycac1
# https://www.fluidsynth.org/
# https://www.fluidsynth.org/api/index.html
# https://github.com/SpotlightKid/pyfluidsynth


# import sys
# import rtmidi
# from rtmidi.midiutil import open_midioutput
# from rtmidi.midiconstants import NOTE_OFF, NOTE_ON

# -------------------------------------------
# - COSTANTI
#   • PCHS (tuple)         = contiene i simboli delle altezze in formato lilypond
#   • DURS (tuple di dict) = {ratio:simbolo}
#   • IDURS (tuple di dict) = {simbolo:ratio}
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

#   • dur2seq(dur=4,bpm=60,beat=4) converte durate da formato lilypond a secondi 
#   • note(pitch=60,dur=1,vel=64,track=0) funzione di utilità
#   • voice(pitch=60,dur=1,vel=64,track=0) suona una sequenza di note o un accordo
#   • voices(([pitchV1],[pitchV2],[...]),  ogni voce è in un nuovo canale
#            ([durV1],  [durV1],  [...])
#            ([velsV1], [velsV2], [...])
#            )
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

    '':          ''        # nessuna espressione
}

# -------------------------------------------
# - FUNZIONI:

def tonalita(key:str=None) -> str:
    """
    Return alteration of key signature.

    :param key: tonalità (es. 'd', 'ef', 'a', 'bf')
    :type key: str or None
    :return: 'diesis' or 'bemoli'
    :return type: str
    """
    if key is None:
        return 'diesis'

    if key in TONALITA_DIESIS:
        return 'diesis'
    else:
        return 'bemoli'
    
# a = tonalita('ef')
# print(a)

def mapPitch(a:list|int, key=None) -> list[str]:
        '''
        Convert int midi pitches in lylipond pitch symbols.
        
        :param a: list of pitches
        :type a: list[int] or int
        :return: list of lilypond pitch symbols
        :rtype: list[str]
        '''
        if type(a) is not list:
            a = [a]

        scegli = tonalita(key)      # Scegli tra 'diesis' e 'bemoli'
                        
        out = []
        for i in a:
            if type(i) is list:      # se accordo
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
                # elif i == 00:           # se valore precedente
                #     out.append('')     
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

# a = [64,[56,89]]    # Sequenza polifonica
# a = mapPitch(a)
# print(a)

#a = [62,[66, 69]]    # Tonalità con diesis
#a = mapPitch(a,k)
#print(a)
#k = 'd'

# a = [63,[67, 70]]    # Tonalità con bemolli
# k = 'ef'
# a = mapPitch(a,k)
# print(a)

def mapDur(a: list | int) -> list[str]:          
        '''
        convert durations in lilypond duration symbols.

        :param a: list of durations
        :type a: list[int] or int
        :return: list of lilypond duration symbols
        :rtype: list[str]
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
                # if i == 00:                  # se 00 valore precedente 
                #     out.append('')         
                # else:
                out.append(DURS[0][1/i]) # se regolare  
        return out 


# a = 4                # Singola durata
# print(a)

# a = [4,8,8]          # Sequenza di durate
# a = mapDur(a)
# print(a)

# a = [4,[4,[7,1,3]]]    # Ritmi puntati o irregolari
# a = mapDur(a)
# print(a)

def mapVel(a:list[int]) -> list[str]:
        ''' 
        Convert list of velocities in lilypond dynamic symbols.

        :param a: list of velocities
        :type a: list[int] or int
        :return: list of lilypond dynamic symbols
        :rtype: list[str]
        '''
        if type(a) is not list:
            a = [a]                     # Casting
        out = []       
        for i in range(len(a)):    
            # if a[i] == 00:
            #     val = a[i-1]
            # else:
            val = a[i]
            if val == 0:
                out.append('')
            elif 1 <= val <= 9:
                out.append(VELS[0])  # ppppp
            elif 10 <= val <= 19:
                out.append(VELS[1])  # pppp
            elif 20 <= val <= 29:
                out.append(VELS[2])  # ppp
            elif 30 <= val <= 39:
                out.append(VELS[3])  # pp
            elif 40 <= val <= 49:
                out.append(VELS[4])  # p
            elif 50 <= val <= 59:
                out.append(VELS[5])  # mp
            elif 60 <= val <= 69:
                out.append(VELS[6])  # mf
            elif 70 <= val <= 79:
                out.append(VELS[7])  # f
            elif 80 <= val <= 89:
                out.append(VELS[8])  # ff
            elif 90 <= val <= 99:
                out.append(VELS[9])  # fff
            elif 100 <= val <= 109:
                out.append(VELS[10]) # ffff
            else: 
                out.append(VELS[11]) # fffff
        return out

# a = 60             # Singola velocity
# a = mapVel(60)
# print(a)

# a = [60,81,102]     # Sequenza di velocities
# a = mapVel(a)
# print(a)

# a = [60,00,81,00,102]     # Sequenza di velocities alternate
# a = mapVel(a)
# print(a)

def mapExp(a:list[str]) -> list[str]:   
        ''' 
        convert list of expressions in lilypond expression symbols.

        :param a: list of expressions
        :type a: list[str] or str
        :return: list of lilypond expression symbols
        :rtype: list[str]
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

def nDim(a:list) -> int:
    '''
    Return list dimension

    :param a: list
    :type a: list
    :return: dimension of the list
    :rtype: int
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

def l_mod(lista: list, target: int)-> list:
    '''
    Generate a list of n elements (target) by repeating the input list and applying modulo.

    :param lista: input list (1D, 2D or 3D)
    :type lista: list
    :param target: desired length of the output list
    :type target: int
    :return: list of length target
    :rtype: list
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

def l_zero(lista:list, target:int) -> list:
    '''
    Generate a list of n elements (target) by repeating the input list and applying zero padding.

    :param lista: input list (1D, 2D or 3D)
    :type lista: list
    :param target: desired length of the output list
    :type target: int
    :return: list of length target
    :rtype: list
    '''
    nl = []
    idx = 0
    for i in range(len(lista)):
        el = lista[i]
        idx += 1
        if nDim(el) == 2:         # Se lista 3D (contiene ritmi irregolari)
            idx += len(el[1])
            idx -= 1
            # if el == 00:
            #      nl.append('')
            # else:
            nl.append(el)
        else:
            # if el == 00:
            #      nl.append('')
            # else:
            nl.append(el)
    for i in range(target-idx):
        nl.append(lista[-1])
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

def dflt(a=None,offset=0):
    '''
    Genera array di default e aggiunge uno zeropad se argomento è:
    • a = None
    • a = int
    • a = lista
    • offset = se a --> None questo è il valore che aggiunge
    '''
    if a is None:                      # SE non esiste
        out = [offset, 'zero']              # ---> mette default
    elif type(a) is not list:          # SE è int singolo
        out = [a, 'zero']              # --> crea una lista
    elif a[-1] != 'mod' and a[-1] != 'zero': # SE è una lista e non specifica il modo
        a.append('zero')                     # --> lo mette di default
        out = a
    else:
        out = a                         # altrimenti lo assegna
    return out
   
# a = None       # Se non specifichiamo argomento
# a = dflt(a)   
# print(a)

# a = 60         # Se specifichiamo singolo int
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
    '''
    Trova il size della lista più lunga
    '''
    idx = 0                      # conteggio esatto elementi in durate
    for i in dur:
        if type(i) == list:                      # se irregolare
            idx = idx + len(i[1])
        else: idx += 1                           # se regolare
    return max(len(note),idx,len(vel),len(exp))  # trova il size max

def dur2sec(dur=4,bpm=60,beat=4):
    '''
    Converte valori espressi in notazione lilypond 
    in valori assoluti in secondi
    
    :param dur: int or list
    :param beat: beat value (1,2,4,8,16,32)
    :param bpm: bpm value
    '''
    beatinsec = 60/bpm    # calcola 1 beat in secondi

    if type(dur) == int:  # se una sola durata
        return beatinsec * (beat/dur)
    else:                 # se è una sequenza
        out = []
        for i in dur:
            if type(i)==int:
                out.append(beatinsec * (beat/i))
            else:
                beatratio = beat/i[0]
                for sudd in i[1]:
                    sudd = sudd * (beatratio / sum(i[1]))    # ratio delle suddivisione
                    out.append(beatinsec*sudd)
        return out
    
# a = dur2sec(8, 60, 4)
# print(a)

# a = dur2sec([8,16,16], 60, 4)

# a = dur2sec([4, [4,[1,1,1]]], 60, 4)
# print(a)

def note(pitch=60,dur=4,vel=64,track=0):
    '''
    Definisce una nota midi.
    Se pitch è un int esegue una sola nota, altrimenti un accordo.
    
    :param pitch: midinote 0-127
    :param vel: midi velocity 0-127
    :param dur: Duration in seconds
    :param track: midi channel default = channel 0
    '''

    if type(pitch) is not list:
        fs.noteon(track, pitch, vel)
    else:
        for i in pitch:
            fs.noteon(track, i, vel)
    
    t.sleep(dur+0.01)   # delta + 10ms per correggere bug python
    if type(pitch) is not list:
        fs.noteoff(track, pitch)
    else:
        for i in pitch:
            fs.noteoff(track, i)

# fs.program_select(0, sfid, 0, 0) # definisce lo strumento
# note(60,2,69) # singola nota
# note([60,64,67,72],2,67) # accordo

def voice(pitch=60,dur=4,vel=64,track=0):
    '''
    Definisce una sequenza a una voce (track) anche polifonica.
    
    :param pitch: list o list2D (accordi)
    :param vel: int or list
    :param dur: int or list
    :param track: default = channel 0
    '''
    
    if type(vel) is not list:
        vel = [vel for _ in range(len(pitch))]
    if type(dur) is not list:
        dur = [dur for _ in range(len(pitch))]
    for i in range(len(pitch)):
        threading.Thread(target=note, kwargs={"pitch": pitch[i],"vel":vel[i],"dur":dur[i],"track":track}).start()
        t.sleep(dur[i])

# fs.program_select(0, sfid, 0, 0) # definisce lo strumento
# pits = [60,  64, 67, [72,73,74]]
# durs = [1,  0.5,0.5, 2]
# vels = [100, 80, 60, 40]

# voice(pits,durs,vels)

def voices(pitch=60,dur=4,vel=4,chan=0):
    '''
    Defininisce più voci. Corrisponde a Staff.
    Mette automaticamente ogni voce in una track (midi channel) diversa.
    
    :param pitch: tuple di liste
    :param vel: tuple di liste
    :param dur: tuple di liste
    '''
    for i in range(len(pitch)):
        threading.Thread(target=voice, kwargs={"pitch": pitch[i],"vel":vel[i],"dur":dur[i],"track":chan[i]}).start()

# fs.program_select(0, sfid, 0, 0)  # strumento voce 1
# fs.program_select(1, sfid, 0, 20) # strumento voce 2

# c1 = (0,                       0)      # canali
# p1 = ([60,  64, 67, [68,72]], [90,     94, 96,  97]) # tuple
# d1 = ([1,  0.5,0.5,  2],      [0.25, 0.25,  1, 0.5])
# v1 = ([100, 80, 60, 40],      [100,   110, 60,  80])

# voices(p1, d1, v1, c1)

# t.sleep(5)
# print("STOP")
# fs.delete()  

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
    def __init__(self, note:int | list | list[list]=60,dur:int | list | list[list]=None,vel:int | list =None,exp:str | list =None,key:str=None) -> None:
        """
        :param note: list of pitches
        :type note: int or list(int or list 2D)
        :param dur: list of duration
        :type dur: int or list(int or list 2D)
        :param vel: list of velocities
        :type vel: int or list
        :param exp: list of expressions
        :type exp: str or list(string)
        :param key: key signature (string) per mapping note (es. 'd', 'ef', 'g', ecc.)
        """

# Assegna le variabili locali e genera eventuali default (dflt())
        self.note = dflt(note, 60)                        # [seq, tipo]
        self.dur  = dflt(dur, 4)   
        self.vel  = dflt(vel, 0)
        self.exp  = dflt(exp, '')
        self.key  = key

        self.note = [self.note[0:-1], self.note[-1]]  # [[seq], tipo] 
        self.dur  = [self.dur[0:-1],  self.dur[-1]]
        self.vel  = [self.vel[0:-1],  self.vel[-1]]
        self.exp  = [self.exp[0:-1],  self.exp[-1]]

# trova il size max delle liste per normalizzazione
        self.max  = getmaxsize(self.note[0],self.dur[0],self.vel[0],self.exp[0]) 

# normalizza la lunghezza delle liste in due modalità 'mod' oppure 'zero'
        self.m_note = selmode(self.note, self.max) 
        self.m_dur  = selmode(self.dur, self.max)  
        if self.vel[0][0] == 0:       # di default mette 64 nel midi
            self.m_vel = selmode([[64],'zero'], self.max)
        else:
            self.m_vel  = selmode(self.vel, self.max)
        self.m_exp  = selmode(self.exp, self.max)

# mapping con liste di simboli lilypond
        self.note = mapPitch(self.m_note, self.key)  
        self.dur  = mapDur(self.m_dur) 
        if self.vel[0][0] == 0:       # di default mette '' nella stampa
            self.vel  = mapVel([0])
        else:
            out = []
            id = 0
            curr = self.m_vel[id]
            next = self.m_vel[id+1]
            for i in self.m_vel:
                if next == curr:
                    out.append(0)
                    next = self.m_vel[np.clip(id+1,0,len(self.m_vel)-1)]
                else:
                    out.append(i)
                    curr = self.m_vel[id]
                id += 1       
            self.vel  = mapVel(out) 
        self.exp  = mapExp(self.m_exp) 
 
# a = _Map(60)
# print(a.m_note)
# print(a.m_dur)
# print(a.m_vel)

# print(a.note)
# print(a.dur)
# print(a.vel)
# print(a.exp)

# p = [60,45,56,[67,78,89],67,56,67,'mod'] # Sequenza monodica
# v = [89,90,90,90,100]
# d = [4,  [4,[3,1]],4,4,8,'zero']
# e = ['.','>','mod']

# a = _Map(p, d, v, e, 'd')

# print(a.m_note)
# print(a.m_dur)
# print(a.m_vel)
# print(a.m_exp)

# print(a.note)
# print(a.dur)
# print(a.vel)
# print(a.exp)

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
                 filename:str="score", format:str="pdf",
                 version:str="2.24.4"
                ) -> None:
        """
        :param filename: filename (without extension), default is "score"
        :type filename: str
        :param format: graphic format for output (pdf, png), default is "pdf"
        :type format: str
        :param version: version of lilypond to use, default is "2.24.4"
        :type version: str
        """
        self.filename  = filename
        self.format    = format
        self.version   = version

    @property
    def print_out(self):
        """
        Print the lilypond output string to the console.-
        """
        self.outo = f"\n\\version \"{self.version}\"\n\\language \"english\"\n\n{self.outstring}"
        print(self.outo)
    
    @property
    def make_file(self):
        """
        Save the lilypond output string to a .ly file and compile it to generate the specified .format and MIDI files.
        """
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
        self.note = ins.note       # recupera da _Map le note per lilypond
        self.m_note = ins.m_note   # recupera da _Map le note per il MIDI
        self.dur  = ins.dur 
        self.m_dur = ins.m_dur
        self.vel  = ins.vel 
        self.m_vel = ins.m_vel
        self.exp  = ins.exp 
        self.music   = ''
        self.id      = -1
        
        for i in self.dur:       # costruisce il formato lilypond
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
    
# a = _Voice(60)
# a.make_file
# print(a.m_note)
# print(a.m_dur)
# print(a.m_vel)

# print(a.note)
# print(a.dur)
# print(a.vel)
# print(a.exp)

# p = [60, 64, 67, 72, 67,76,67,69]      # Sequenza monofonica ritmo regolare
# d = [ 8, 16, 16,  4, 'mod']
# v = [60, 80, 80, 80, 'zero']
# e = ['.','.','.','', '>','zero']

# a = _Voice(p,d,v,e,'acci')
# a.make_file

# a = _Voice(p,d,v,e,filename='acci')
# a.make_file

# p = [60,64,67,[64,72,75],67,76,67,69,71,'mod'] # Sequenza polifonica ritmo regolare
# d = [ 8,16,16, 4, 16,16,16,16,16,16,8,'mod']
# v = [60,0,0,90, 'zero']
# e = ['.','.','.','','>','zero']

# a = _Voice(p,d,v,e)
# a.make_file

# p = [60, 64, 67,     72,67,76, 67, 69, 71]      # Sequenza monofonica ritmo irregolare
# d = [ 8, 16, 16, [4,[2, 1, 2]], 'mod']
# v = [60,     00,00,90,'zero']
# e = ['cresc',00,00,'dim',00,00,00,'end']

# a = _Voice(p,d,v,e)
#a.make_file

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
                 note:int | list[int]=60,dur:int | list[int]=None,vel:int|list[int]=None,exp=None,
                 key:str=None,t_sig:str=None,clef:str=None,
                 i_name:str=None,i_short:str=None,i_midi:str=None,
                 filename:str="score", format:str="pdf", version:str="2.24.3"
                 ):
        """
        :param note: list of pitches
        :type note: int or list(int or list 2D)
        :param dur: list of duration
        :type dur: int or list(int or list 2D)
        :param vel: list of velocities
        :type vel: int or list
        :param exp: list of expressions
        :type exp: str or list(string)
        :param key: key signature
        :type key: str
        :param t_sig: time signature
        :type t_sig: str
        :param clef: clef
        :type clef: str
        :param i_name: instrument name for score
        :type i_name: str
        :param i_short: short instrument name for score
        :type i_short: str
        :param i_midi: MIDI instrument name for score
        :type i_midi: str
        :param filename: filename (without extension), default is "score"
        :type filename: str
        :param format: graphic format for output (pdf, png), default is "pdf
        :type format: str
        :param version: version of lilypond to use, default is "2.24.3
        :type version: str
        """

        super().__init__(filename,format,version)

        self.note = note  # note in input
        self.dur  = dur
        self.vel  = vel
        self.exp  = exp
        self.key  = key
        self.t_sig = t_sig

        self.voice = []      # Lista di Voice per print
        self.m_voice = []    # lista di Voice per MIDI
        if type(note) == tuple: 

            for i, _ in enumerate(note):
                voicedur = None if self.dur is None else self.dur[i]
                voicevel = None if self.vel is None else self.vel[i]
                voiceexp = None if self.exp is None else self.exp[i]

                a = _Voice(self.note[i], voicedur, voicevel, voiceexp, self.key)
                self.voice.append(a.out)
                self.m_voice.append(a)
        else:
            self.voice.append(_Voice(self.note,self.dur,self.vel,self.exp,self.key).out)
            self.m_voice.append(_Voice(self.note,self.dur,self.vel,self.exp,self.key))

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
            (f"\t\t\t\t  \\key {self.key} \\major\n"                       if self.key   else "") +
            (f"\t\t\t\t  \\numericTimeSignature\n"                    if self.t_sig else "") +
            (f"\t\t\t\t  \\time {self.t_sig}\n"                            if self.t_sig else "") +
            f"\t\t\t{self.vseq}\n" +
            "\t\t}"
        )

    @property
    def out(self):
        """
        Return the lilypond output string for the staff.
        """
        return self.outstring

    def play(self,bpm=60,beat=4,chan=0,instrID=0, audioDev:str='coreaudio', sf2_abs_path:str=None):   # Sistema instr e canale
        '''
        Converte durate in durate assolute
        Esegue una sequenza
    
        :param pitch: int    = nota singola
                      list   = sequenza monofonica
                      list2D = sequenza polifonica o singolo accordo
                      tuple  = sequenza di più voci
        :param vel: int      = nota singola
                    list     = sequenza
                    tuple  = sequenza di più voci 
        :param dur: int      = nota singola
                    list     = sequenza
                    tuple  = sequenza di più voci
        :param bpm: int = tempo metronomico
        :param beat:     = valore del beat (1,2,4,8,16,32)
        '''
        fs = fluidsynth.Synth()
        fs.start(driver = audioDev)  # dsound (Windows)
        sfid = fs.sfload(sf2_abs_path) # path assoluto file.sf2

        if type(self.note) == int:       # se è una nota singola di una sola voce
            fs.program_select(chan, sfid, 0, instrID) # chan, file.sf2, bank_num, preset_number
            dura = dur2sec(self.m_voice[0].m_dur[0],bpm,beat)       # converte le durate
            note(pitch=self.m_voice[0].m_note,dur=dura,vel=self.m_voice[0].m_vel[0],track=chan) # richiama la funzione note  
            t.sleep(2)   # aspetta 1 secondo      
            print("STOP")
            fs.delete()  
        # FONO A QUA FUNZIONA
        elif type(self.note) == list:      # se è una sequenza a una voce o accordo 
            fs.program_select(chan, sfid, 0, instrID) # chan, file.sf2, bank_num, preset_number
            dura = dur2sec(self.m_voice[0].m_dur,bpm,beat)        # converte le durate
            voice(pitch=self.m_voice[0].m_note,dur=dura,vel=self.m_voice[0].m_vel,track=chan) # richiama la funzione voice     
            t.sleep(2)   # aspetta 1 secondo
            print("STOP")
            fs.delete()  
    # se più voci trova quella che dura di più e fa uno sleep per poi stoppare 
    # la sequenza e distruggere l'istanza di synth
        else:                        # se è una tuple (più voci)
            t.sleep(0.1)             # correzione bug python
            cpit = []
            cdur = []
            cvel = []
            chans = []
            n = 0
            for i in self.m_voice:
                cpit.append(i.m_note)
                cdur.append(dur2sec(i.m_dur,bpm,beat))
                cvel.append(i.m_vel)
                chans.append(n)     # ogni voce in un midi channel diverso
                # ogni channel con un instrID diverso
                fs.program_select(n, sfid, 0, instrID[n]) # chan, file.sf2, bank_num, preset_number
                n += 1
            voices(pitch=cpit,dur=cdur, vel=cvel,chan=chans)  
            tdur = []                # Trova la sequenza con durata maggiore
            for i in cdur:
                tdur.append(sum(i)) 
                maxdur = max(tdur)
            t.sleep(maxdur + 2)      # durata massima + 1 secondo per fadeout
            print("STOP")
            fs.delete()   

# a = Staff(60)
# a.make_file
# a.play()

# p = [61,64,67,73,67,76,67,69,76,66,64]      # Sequenza monofonica ritmo regolare
# d = [ 8,16,16, 8, 'mod']
# v = [30,90,49, 'zero']
# e = ['.','.','.','>','zero']

# a = Staff(p,d,v,e,key='d',t_sig='3/4',clef='G',i_name='Ciccio')

# a.make_file
# a.play()

# p = [61,[64,67],73,[67,76],67,[69,76,66],64,60,'mod']  # Sequenza polifonica ritmo regolare
# d = [ 8,16,16, 8, 'mod']
# v = [60,80,90, 'zero']
# e = ['.','.','.','>','zero']

# a = Staff(p,d,v,e,key='e',t_sig='3/8',clef='G',i_name='Ciccio')
# a.make_file
# a.play()

# p = [61,64,67,73,67,76,67,69,76,66,64]      # Sequenza monofonica ritmo irregolare
# d = [ [8,[1,1,1]],8,[8,[2,1,2]], 'mod']
# v = [60,80,100,90, 'zero']
# e = ['.','.','.','>','zero']

# a = Staff(p,d,v,e,key='bf',t_sig='5/8',clef='C',i_name='Ciccio')
# a.make_file
# a.play()

# p = [61,[64,67],73,[67,76],67,[69,76,66],64,60,87,76,65,'mod']  # Sequenza polifonica ritmo itregolare
# d = [ [8,[1,1,1]],8,[8,[2,1,2]], 'mod']
# v = [60,80,90,100, 'zero']
# e = ['.','.','.','>','zero']

# a = Staff(p,d,v,e,key='e',t_sig='2/4',clef='G',i_name='Ciccio')
# a.make_file
# a.play()

# Sequenza polifonica ritmo irregolare

# instr = [0, 1]   # Strumenti midi

# pa = [61,[64,67],73,[67,76],67,[69,76,66],64,60,87,76,65,'mod']  
# da = [ [8,[1,1,1]],8,[8,[2,1,2]], 'mod']
# va = [60,80,90, 'zero']
# ea = ['.','.','.','>','zero']

# pb = [56,54,52]
# db = [4,  4, 4]
# vb = [90,90,90]
# eb = ['','','']

# p = (pa,pb) # tuple di liste
# d = (da,db)
# v = (va,vb)
# e = (ea,eb)

# a = Staff(p,d,v,e,key='e',t_sig='2/4',clef='G',i_name='Ciccio')
# a.make_file
# a.play(instrID=instr)

class Score(_Print):
    '''
        Definisce le caratteristiche della partitura. 
        Formattando gli outputs delle classi precedenti. 
        Di default crea uno StaffGroup.
        IN: • staff (tuple di output di una o più istanze di Staff)
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
                 staff:str="\n\t\t{c' d' e' f'}",
                 staff_size:int=None, indent:int=None, s_indent:int=None,
                 title:str=None, composer:str=None,
                 size:str="a4landscape", margins:tuple=(10,10,10,10),
                 filename:str="score", format:str="pdf", version:str="2.24.3"    # ereditati da _Print
                ) -> None:
        """
        Constructor for Score class.

        :param staff: tuple of Staff outputs or single Staff output, default is a simple staff with c' d' e' f'
        :type staff: str or tuple of str in lilypond format
        :param staff_size: staff size in mm, default is None (standard size)
        :type staff_size: int or None
        :param indent: indent in mm, default is None (no indent)
        :type indent: int or None
        :param s_indent: short indent in mm, default is None (no short indent)
        :type s_indent: int or None
        :param title: title of the score, default is None (no title)
        :type title: str or None
        :param composer: composer of the score, default is None (no composer)
        :type composer: str or None
        :param size: page size, default is "a4landscape". Can be a predefined size string or a tuple of two ints for custom width/height in mm  
        :type size: str or tuple(int, int)
        :param margins: page margins as a tuple (top, bottom, left, right) in mm, default is (10, 10, 10, 10)
        :type margins: tuple(int, int, int, int)
        :param filename: filename (without extension), default is "score"
        :type filename: str
        :param format: graphic format for output (pdf, png), default is "pdf"
        :type format: str
        :param version: version of lilypond to use, default is "2.24.3"
        :type version: str
        """

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


# staffa = (a, b) # Tuple di Staff

# a = Score(staffa,title='ammazza', composer='stika',staff_size=[2,3]).make_file

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