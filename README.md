# Brief-2C - backend

Dépendances Requise:
  - hug
  - psycopg2
  - SQLAlchemy
  - 
  - Voir requirements.txt  

Lancer le server dans l'environement venv:
  - .venv/Script/Activate.ps1
    - hug -f server.py (lance le serveur hug)
    - py database/database.py (lance les migration)

[venv]

...

user     = ...
password = ...
database = ...

à ajouter dans pyvenv.cfg
