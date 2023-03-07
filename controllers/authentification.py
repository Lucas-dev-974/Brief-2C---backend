import hug
import jwt
from hashlib import sha512
import secrets

from database.database import session
from database.entity import Users

# Fonctions-------------------------------------------------------

# Vérifie le token => précisement comment ??
def token_verify(token):
    global secret_key
    try:
        return jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.DecodeError:
        return False

# Hashe un mdp
def hashage(mdp:str):
    # salt = secrets.token_hex(24).encode()
    salt = b'f2937e3b3837325367839443aa583ca7b8c904029ce5a1f4' # Permet d'augementer la "force" du hashage

    mdp = mdp.encode() # string => bytes
    
    # Hashage
    mdp_hashe = sha512(salt + mdp).hexdigest()

    return mdp_hashe

# Variables globales --------------------------------------------

secret_key = "1bc3851624fa399d46350929f20dd5610d0aa5994b621d69"

token_key_authentication = hug.authentication.token(token_verify)

# API------------------------------------------------------------

# Authentification
@hug.post('/login')
def token_gen_call(username, password):
    """Authentifier et renvoyer un token"""
    global secret_key

    # Vérif que le username est présent dans la BDD
    usernameExist = session.query(Users.username).where(Users.username == username).count()
    if usernameExist == 0:
        return "Nom d'utilisateur et/ou mot de passe incorrect"
    
    elif usernameExist == 1:
        # Récuperer le vrai mdp
        realPwd = session.query(Users.password).where(Users.username == username).value(Users.password)

        # Vérifier la corespondance
        if secrets.compare_digest(realPwd, hashage(password)): # Plus securisé que simple vraiMdp == mdpEntre car temps de comparaison constant (timing attacks)
            return {"token" : jwt.encode({'user': username}, secret_key, algorithm='HS256')}
        else:
            return "Nom d'utilisateur et/ou mot de passe incorrect"


# Test restriction d'accès
@hug.get('/token_authenticated', requires=token_key_authentication)
def token_auth_call(user: hug.directives.user):
    ''' Test restriction d'accès, fonctionel '''
    return '"Test requête GET ": You are user: {0}'.format(user['user'])

# Ajout d'utilisateur
@hug.post('/register')
def register(username, password):
    ''' Enregistrer un nouvel utilisateur  '''
    # Vérif username n'éxiste pas déjà
    usernameAlreadyExist = session.query(Users).where(Users.username == username).count()
    if usernameAlreadyExist == 1:
        return 'Nom d\'utilisateur déja pris'
    # Enregistrements des identifiants
    else :
        session.add(Users(username = username, password = hashage(password)))
        session.commit()
        return 'ok'