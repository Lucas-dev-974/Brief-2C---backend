import hug
import jwt

# Authentification ---------------------------------
secret_key = "secret_key" # À modif...

def token_verify(token):
    global secret_key
    try:
        return jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.DecodeError:
        return False
    

# Authentification
@hug.post('/login')
def token_gen_call(username, password):
    """Authentifier et renvoyer un token"""
    global secret_key
    usernameTest = 'admin' # Ici username et pwd à vérif depuis la BDD !
    pwdTest      = 'admin'

    if username == usernameTest and password == pwdTest:
        return {"token" : jwt.encode({'user': username}, secret_key, algorithm='HS256')}
    else:
        return "Nom d'utilisateur et/ou mot de passe incorrect"
    
token_key_authentication = hug.authentication.token(token_verify)

@hug.get('/token_authenticated', requires=token_key_authentication)
def token_auth_call(user: hug.directives.user):
    return '"Test requête GET ": You are user: {0}'.format(user['user'])