from __future__ import annotations
import numpy as np
import numbers
from typing import Literal
from collections.abc import Sequence
from fractions import Fraction
from musicnpy import _Set

NUMERIC = numbers.Real
ARRAYLIKE = Sequence[NUMERIC] 
INDEX = int | slice | Sequence[int] 

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

class Pattern:
    
    """
    Handles lists of durations.

    :values: a list of durations, 1 dimension or 3 dimensions. 
            Accepted durtion values:
            :note durations:                [1,2,4,8,16,32]
            :irregular groups subdivisions: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
    :Example:

    >>> p = Pattern([4,8,4,4,16])
    >>> p.vals
    """

    def __init__(self,values: ARRAYLIKE, t_sig: str = '4/4'):
        """
        Define Rythm pattern.

        :param values: a list of durations, 1 dimension or 3 dimensions.
        :type values: list
        :param t_sig: time signature of the pattern, default is '4/4'
        :type t_sig: str
        """
        # super().__init__(values)

        # esprimere durate in durate assolute e durate relative
        # fare check formato VALS
        # problema quantizzazione
        self.set = values
        self.t_sig = t_sig
        self.t_sig_value = eval(t_sig)
        self.vals = self.set.copy()
        self.allowed1d2d = [1,2,4,8,16,32] ## per durate normali o durate di gruppetti
        self.allowed3d = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]## per ritmi irregolari 
        self.dim = nDim(self.set)
        self._guard(self.vals,self.allowed1d2d)
        # print(self.vals)
    
    @property
    def getdim(self): ## check dimensioni
        self.dim = nDim(self.vals)
        return self.dim
    
    def _guard(self,list_in= None, allowed= None): ## possiamo usare questa funzione per prendere anche altre informazioni dalla lista in ingresso
        if self.dim == 1:
            mask = np.isin(list_in, allowed)
            if not all(mask):
                raise ValueError('Error Duration: Invalid duration elements found: must be in format [1,2,4,8,16,32]')
            
        elif self.dim == 3:
            mask = [isinstance(x, list) for x in list_in]
            self.vals = np.array(self.vals,dtype=object) ## quando l'array è multidim lo trasformo in np con objects
            for el in enumerate(list_in):
                if mask[el[0]]:
                    mask_3d = np.isin(el[1][1], self.allowed3d)
                    if not all(mask_3d):
                        raise ValueError('Error Duration: Invalid duration elements found: must be in format [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]')
            
                    if not np.isin(el[1][0],allowed):
                        raise ValueError('Error Duration: Invalid duration elements found: must be in format [1,2,4,8,16,32]')
                else:
                    if not np.isin(el[1],allowed):
                        raise ValueError('Error Duration: Invalid duration elements found: must be in format [1,2,4,8,16,32]')
        else:
            raise ValueError('Error Dimensions: Invalid list dimensions: must be 1 or 3')  
    
    def gen(self, length= 8, type: Literal[None, 'wrap', 'fold', 'clip', 'rand', 'randnd'] = 'rand', mask: list = None):

        if mask == None:
            mask = [1] * (len(self.vals))
            

        percent = list(map(round,mask*1/np.sum(mask)*100))
        rule = np.repeat(self.vals,percent)
        pat = []

        if type == 'rand':
            ## qui va scritto il ciclo dove se self.dim è 3 va a 
            ## guardare dentro i vari livelli secondo l'array [0,0,0]
            ## Capire come mettere l'array dei livelli dentro la funzione gen
            if self.dim == 1:
                rule = _Set(rule)
                pat = rule.getseq(length=length,type=type)

            elif self.dim == 3:
                pat = np.random.choice(rule, length, True) ## true o false non funzionano perchè uso il metodo rule 
                pat = pat.tolist()

                for el in enumerate(pat): ## gestisce i gruppetti generati
                    if isinstance(el[1],list):
                        dur = el[1][0]
                        form = _Set(el[1][1])
                        form = form.getseq(length=len(form),type=type)
                        group = [dur,form]
                        pat[el[0]] = group
                        # print(group)
                    else: 
                        # print(el[1])
                        pass

            else:
                raise ValueError('Error Dimensions: Invalid list dimensions: must be 1 or 3')

            
        elif type != 'rand':
            idx= [0,len(self.vals)-1]

            if self.dim == 1:

                pat = _Set(self.vals).getseq(length=length,type=type)

                

            elif self.dim == 3:
                ## Qui dobbiamo riscrivere le funzioni che ci sono in getseq
                ## per farle funzionare con le jagged lists e decidere i vari comportamenti
                if type == "wrap":
                    for i in range(length):
                        idVal = (i % abs((idx[1]+1) - idx[0])) + idx[0]
                        pat.append(self.vals[idVal])

                    # raise ValueError('Sorry not yet developed :(')
                    
                if type == "fold":
                    INDEX = idx[0]
                    dir = 1
                    for _ in range(length):
                        pat.append(self.vals[INDEX])
                        INDEX += dir
                        if INDEX == idx[1] or INDEX == idx[0]:
                            dir *= -1
                    # raise ValueError('Sorry not yet developed :(')
                    
                if type == "clip":

                    for i in range(length):
                        idVal = i + idx[0]
                        if idVal >= idx[1]:
                            idVal = idx[1]
                        pat.append(self.vals[idVal])

                    # raise ValueError('Sorry not yet developed :(')
                    
                if type == "randnd":
                    # if(length <= len(self.vals)):
                    #     pat = np.random.choice(self.vals, length, False)
                    # else:
                    #     print('Invalid lenght, ecceded list lenght')
                    raise ValueError('Sorry not yet developed :(')
                    
            else:
                raise ValueError('Error Dimensions: Invalid list dimensions: must be 1 or 3')

        return pat
   
def grid(durs, pitches, t_sig='4/4'):

    tsig = eval(t_sig)
    result = []
    misura_corrente = []
    exp = []
    note_rimanenti = []
    
    # Convertiamo la durs di divisori in frazioni reali (es. 4 -> 1/4)
    for d in durs:
        if isinstance(d,int):
            note_rimanenti.append([Fraction(1, d)])
        elif isinstance(d, list):
            # note_rimanenti.append(Fraction(1, d[0]))
            note_rimanenti.append([Fraction(1,d[0]),d])
            # print([Fraction(1,d[0]),d])
    
    spazio_libero = Fraction(tsig)

    i = 0
    while i < len(note_rimanenti):
        durata_nota = note_rimanenti[i]
        if durata_nota[0] <= spazio_libero:
            # La nota sta nella misura (o la riempie esattamente)
            misura_corrente.append(durata_nota[len(durata_nota)-1])
            spazio_libero -= durata_nota[0]
            i += 1 # Passiamo alla nota successiva
            if len(durata_nota) < 2:
                exp.append('')
            else: 
                exp = exp + len(durata_nota[1][1])*['']
            if spazio_libero == 0:
                result.append(misura_corrente)
                misura_corrente = []
                spazio_libero = Fraction(t_sig)
        else:
            # La nota è troppo lunga: va spezzata
            # 1. Prendiamo quello che serve per riempire la misura
            misura_corrente.append(spazio_libero)
            result.append(misura_corrente)
            # 1.1 Aggiungo l'altezza corrente alla nota generata successiva
            # e aggiungo una legatura di valore
            
            if i < len(pitches):
                pitches.insert(i, pitches[i])
            elif pitches: # se la lista pitches non è della stessa lungezzza delle durate 
                pitches.append(pitches[-1])

            exp.append("tie")
            # 2. Calcoliamo quanto resta della nota
            resto_durata = durata_nota[0] - spazio_libero
            
            # 3. Aggiorniamo la nota corrente nella durs con il resto
            # e NON incrementiamo 'i', così al prossimo giro processiamo il resto
            note_rimanenti[i] = [resto_durata]
            
            # Reset misura
            misura_corrente = []
            spazio_libero = Fraction(tsig)

    # Aggiunge l'ultima misura se non è vuota o completa
    if misura_corrente:
        result.append(misura_corrente)

    res = []
    for misura in result:
        for f in misura:
            if isinstance(f,Fraction):
                if f.numerator == 1:
                    res.append(f.denominator)
                else:
                    res.append(f.numerator/f.denominator)
            elif isinstance(f,list):
                res.append(f)

    # Riconvertiamo in divisori per LilyPond (es. 1/4 -> 4)
    # Nota: se la frazione non è standard (es. 3/8), LilyPond richiede sintassi diverse
    return res,exp,pitches



# # a = Pattern([4,[4,[1,3]],8]).gen(11,type="wrap")
# # print(a)

# # # n = Pattern([2,4,8,16])
# # # b = n.gen(11,'rand',[0.1,0.5,0.2,0.4])

# # res,exp,pitches = grid(a,[60,61,62,63])
# # # print(res)
# # # print(b)
# # print(res,exp,pitches)



# # p = pitches+['mod']  # Sequenza polifonica ritmo itregolare
# # d = res+['mod']
# # v = [60,80,00,90, 'zero']
# # # e = [00,'zero']
# # e = exp+['zero']

# # a = Staff(p,d,v,e,key='e',t_sig='4/4',clef='G',i_name='polizia').out
# # score = Score(a,filename="scoreScore.pdf",format="pdf").make_file


# # p = [60,60,60,60,60,60,60,60]  # Sequenza polifonica ritmo itregolare
# # d = [el for sub in res for el in sub]
# # d = [4, 4,4 , [2,[1,3]], 4, 4, 4, 4, 4, 4, 4, 4]
# # v = [60,80,00,90, 'zero']
# # e = ['.','.','.',00,'>','zero']

# # a = Staff(p,d,v,e,key='e',t_sig='4/4',clef='G',i_name='polizia').make_file

# # print(b)
# # b = a.gen()          
# # b = a.sort('r').vals

# # print(b) 
# # c = np.array([[8,[1,1,1,1]],8,[8,[2,1,2]]])
# # print(list(map(round,[0.2,0.3,0.9,0.7]*1/np.sum([0.2,0.3,0.9,0.7])*100)))

# # print(np.array([1,2,[3,[1,1,1]]],dtype=object))

# # v = np.array([4,2,[8,[3,1,1]],16],dtype=object)


# # print(m,v)


# from musicnpy import *
# # a = Scale.new(ScaleModel.maj, 60).to_range(36, 48)
# # print(a)

# a = _PSet([9, 0, 7, 1], 60)
# print(a.intervals)