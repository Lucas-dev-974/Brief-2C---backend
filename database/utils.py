import configparser

# Permet de garder les identifiants de connexion de la BDD dans l'environnement
def getConfig(name):
    config = configparser.ConfigParser()
    config.read('.venv/pyvenv.cfg')       
    
    return config.get('venv', name)