import hug
import jwt

# Authentification ---------------------------------
secret_key = "secret_key" # À modif...

# Authentification
@hug.post('/login')
def token_gen_call(username, password):
    """Authentifier et renvoyer un token"""
    global secret_key
    usernameTest = 'admin' # Ici username et pwd à vérif depuis la BDD !
    pwdTest = 'admin'
    if username == usernameTest and password == pwdTest:
        return {"token" : jwt.encode({'user': username}, secret_key, algorithm='HS256')}
    else:
        return "Nom d'utilisateur et/ou mot de passe incorrect"