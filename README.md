# musicnpy
Libreria composizione assistita

## setup
```
~ cd musicnpy/
~ python3.13 -m venv venv
~ source ./venv/bin/activate
~ pip install -r requirements.txt
```

## run test
```
~ python test.py
```

## compile docs
```
~ cd ./docs/
~ make clean html latexpdf
```

Per compilare il file latex e creare il pdf della documentazione serve ``mactex`` o un compilatore LaTeX.

La documentazione è disponibile in due formati e si troverà all'interno della cartella `./docs/build/`. E' disponibile al [link](https://dvddmg.github.io/musicnpy)