import configparser

def getConfig(name):
    config = configparser.ConfigParser()
    config.read('.venv/pyvenv.cfg')       
    
    return config.get('venv', name)