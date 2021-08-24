# Interrogazioni

Interrogazioni è un sito web che serve a visualizzare comodamente le persone interrogate in alcune materie.

## Installazione

Per prima cosa bisogna installare i requirements (contenuti nel file `requirements.txt`), ad esempio così

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Poi bisogna creare due file:
1. `application/password.txt`: Deve contenere la password di admin
2. `application/students.txt`: Deve contenere la lista di studenti, con uno studente per linea (serve solo in mancanza di `application/data.dat`, un file generato automaticamente)

Fatto ciò, basterà avviare il file `run.py` per avviare il server in debug mode sulla porta 8080.

```bash
python run.py
```

## Autori

* [@gianluparri03](https://github.com/gianluparri03)
* [@Caesar-7](https://github.com/Caesar-7)
* [@EnryBarto](https://github.com/EnryBarto)
* [@TommyAnd](https://github.com/TommyAnd)
