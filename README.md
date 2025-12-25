# musicnpy
Libreria composizione assistita

## setup
```
~ cd musicnpy/
~ python3.13 -m venv venv
~ source ./venv/bin/activate
~ pip install -r requirements.txt
```

## compile
```
~ cd ./docs/
~ make clean html latexpdf
```

Per compilare il file latex e creare il pdf della documentazione serve ``mactex`` o un compilatore LaTeX.

## run test
```
~ python test.py
```