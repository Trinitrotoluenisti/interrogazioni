# Interrogazioni

Interrogazioni serve a gestire le liste delle interrogazioni di una classe.
O perlomeno questa era l'idea iniziale.

## Come si fa partire

1. Installa flask.
2. Crea un file chiamato `application/admin_password.py` con dentro una variabile `ADMIN_PASSWORD` contenente la password di admin.
3. Crea un file `application/data.json` tipo questo

```json
{
    "lists": {},
    "elements": {
        "1": {
            "id": 1,
            "name": "Studente 1"
        },
        "2": {
            "id": 2,
            "name": "Studente 2"
        },
        "3": {
            "id": 3,
            "name": "Studente 3"
        }
    }
}
```

4. Fai partire `run.py`.

## Come si usa

Dovrebbe essere intuitivo.

## Chi l'ha fatto

[@gianluparri03](https://github.com/gianluparri03), [@Caesar-7](https://github.com/Caesar-7), [@EnryBarto](https://github.com/EnryBarto) e [@TommyAnd](https://github.com/TommyAnd).
I [Trinitrotoluenisti](https://github.com/Trinitrotoluenisti), per farla breve.
