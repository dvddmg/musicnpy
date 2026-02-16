from __future__ import annotations
import numpy as np
from fractions import Fraction
import numbers, operator
from typing import Self, TypeAlias, Callable, Any, Literal 
from collections.abc import Sequence, Iterator
from musicnpy import _Set


Numeric = numbers.Real
ArrayLike = Sequence[Numeric]
Index = int | slice | Sequence[int]


class Pattern(_Set):
    def __init__(self,values = ArrayLike, bpm= 60, t_sig = 4/4):
        # super().__init__(values)

        # esprimere durate in durate assolute e durate relative
        # fare check formato VALS
        # problema quantizzazione
        self.set = values
        self.vals = self.set.copy()
        self.allowed1d2d = [1,2,4,8,16,32] ## per durate normali o durate di gruppetti
        self.allowed3d = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]## per ritmi irregolari 
        self.dim = nDim(self.set)
        self.guard(self.vals,self.allowed1d2d)
        # print(self.vals)
    
    @property
    def getdim(self): ## check dimensioni 
        self.dim = nDim(self.vals)
        return self.dim
    
    def guard(self,list_in= None, allowed= None): ## possiamo usare questa funzione per prendere anche altre informazioni dalla lista in ingresso
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
        rule = np.repeat(self.vals,percent).tolist()
        # rule = _Set(rule)

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
            if self.dim == 1:

                pat = _Set(self.vals).getseq(length=length,type=type)
               
            elif self.dim == 3:
                ## Qui dobbiamo riscrivere le funzioni che ci sono in getseq
                ## per farle funzionare con le jagged lists e decidere i vari comportamenti
                if type == "warp":
                    raise ValueError('Sorry not yet developed :(')
                    
                if type == "fold":
                    raise ValueError('Sorry not yet developed :(')
                    
                if type == "clip":
                    raise ValueError('Sorry not yet developed :(')
                    
                if type == "randnd":
                    raise ValueError('Sorry not yet developed :(')
                    
            else:
                raise ValueError('Error Dimensions: Invalid list dimensions: must be 1 or 3')
            

 
        return pat
        

    # def profile(self):

    # def morph(self, otherlist):
        
    # def negative(self):

    # def substitute(self): # oppure aggiungere la funzione setitems in _Set


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

def grid(lista, pitches, t_sig=1):
    result = []
    misura_corrente = []
    exp = []
    
    # Convertiamo la lista di divisori in frazioni reali (es. 4 -> 1/4)
    note_rimanenti = [Fraction(1, d) for d in lista]
    
    spazio_libero = Fraction(t_sig)
    
    i = 0
    while i < len(note_rimanenti):
        durata_nota = note_rimanenti[i]
        
        if durata_nota <= spazio_libero:
            # La nota sta nella misura (o la riempie esattamente)
            misura_corrente.append(durata_nota)
            spazio_libero -= durata_nota
            i += 1 # Passiamo alla nota successiva
            exp.append(00)
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
            pitches.insert(i,pitches[i])
            exp.append('tie')
            # 2. Calcoliamo quanto resta della nota
            resto_durata = durata_nota - spazio_libero
            
            # 3. Aggiorniamo la nota corrente nella lista con il resto
            # e NON incrementiamo 'i', così al prossimo giro processiamo il resto
            note_rimanenti[i] = resto_durata
            
            # Reset misura
            misura_corrente = []
            spazio_libero = Fraction(t_sig)

    # Aggiunge l'ultima misura se non è vuota o completa
    if misura_corrente:
        result.append(misura_corrente)

    res = []
    for misura in result:
        for f in misura:
            if f.numerator == 1:
                res.append(f.denominator)
            else:
                res.append(f.numerator/f.denominator)

    # Riconvertiamo in divisori per LilyPond (es. 1/4 -> 4)
    # Nota: se la frazione non è standard (es. 3/8), LilyPond richiede sintassi diverse
    return res,exp,pitches


# a = Pattern([4,4,[4,[1,1,1]],8])

# n = Pattern([2,4,8,16])
# b = n.gen(11,'rand',[0.1,0.5,0.2,0.4])

# res,exp,pitches = grid(b,[61,[64,67],73,[67,76],67,[69,76,66],64,60,87,76,65])
# print(b)
# print(res,exp,pitches)



# p = pitches+['mod']  # Sequenza polifonica ritmo itregolare
# d = res+['mod']
# v = [60,80,00,90, 'zero']
# # e = [00,'zero']
# e = exp+['zero']

# a = Staff(p,d,v,e,key='e',t_sig='4/4',clef='G',i_name='polizia').make_file


# print(np.unique([1,1,2,2,3,4,4,4,5,6,7]))

# p = [60,60,60,60,60,60,60,60]  # Sequenza polifonica ritmo itregolare
# d = [el for sub in res for el in sub]
# d = [4, 4,4 , [2,[1,3]], 4, 4, 4, 4, 4, 4, 4, 4]
# v = [60,80,00,90, 'zero']
# e = ['.','.','.',00,'>','zero']

# a = Staff(p,d,v,e,key='e',t_sig='4/4',clef='G',i_name='polizia').make_file

# print(b)
# b = a.gen()          
# b = a.sort('r').vals

# print(b) 
# c = np.array([[8,[1,1,1,1]],8,[8,[2,1,2]]])
# print(list(map(round,[0.2,0.3,0.9,0.7]*1/np.sum([0.2,0.3,0.9,0.7])*100)))

# print(np.array([1,2,[3,[1,1,1]]],dtype=object))

# v = np.array([4,2,[8,[3,1,1]],16],dtype=object)


# print(m,v)
    


    # def profile(self):

    # def morph(self, otherlist):
        
    # def negative(self):

    # def substitute(self): # oppure aggiungere la funzione setitems in _Set

# a = Pattern([4, 8, 16, 16, 4])
# a = a.getseq(length=16, type='rand')
# print(a)

# b = Pattern([4, [8, [1, 1, 1]]])
# print(b)

# a = Pattern([2, 4, 4, 8, 16, [4, [1, 2, 4, 3, 15]]]).gen(25)
# print(a)


# a = Pattern([2, 8, 2, 2, 2, 6, 4, 2, 2])
