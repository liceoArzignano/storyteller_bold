Storyteller Bold
====

### Requisiti
* python3
* pip

### Dipendenze

Le dipendenze sono specificate nel file _requirements.txt_.  
Per installarle esegui il comando
```
pip install -r requirements.txt
```

### Configurazione

È necessario definire una variabile contentente la chiave api del progetto firebase da utilizare:
```
export SNAKE_API_KEY="000000000000000000000000000000000000000"
```

### Utenti

Per aggiungere un utente, è necessario creare un database di firebase contentente un nodo figlio "users" con al suo interno i vari utenti, definiti nel formato chiave:valore di username:password

### Utilizzo

Eseguire lo script tramite il comando

```
python3 main.py
```

In seguito, aprire l'indirizzo riportato nel browser (di default dovrebbe essere _localhost:5000_)

