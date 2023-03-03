import hug
from hug.middleware import CORSMiddleware
from database.entity import Models
import os 
import falcon
import jwt
import subprocess
from database.database import session
from controllers import authentification

api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api, allow_origins=['*'])) # allow_origins à restreindre pour le déploiement

api.extend(authentification, '/api/authentication')

# Labo subprocess------
# subprocess.run()

# python_path = '../.venvtest/Scripts/python.exe'

# script_path = '../testKeras.py'

# command = [python_path, script_path]

# output = subprocess.check_output(command)
# print(output)
#---------------------------------------------------

# Authentification ---------------------------------
# secret_key = "secret_key" # À modif...

def token_verify(token):
    global secret_key
    try:
        return jwt.decode(token, secret_key, algorithms=['HS256'])
    except jwt.DecodeError:
        return False

token_key_authentication = hug.authentication.token(token_verify)

# # Authentification
# @hug.post('/api/login')
# def token_gen_call(username, password):
#     """Authentifier et renvoyer un token"""
#     global secret_key
#     usernameTest = 'admin' # Ici username et pwd à vérif depuis la BDD !
#     pwdTest = 'admin'
#     if username == usernameTest and password == pwdTest:
#         return {"token" : jwt.encode({'user': username}, secret_key, algorithm='HS256')}
#     else:
#         return "Nom d'utilisateur et/ou mot de passe incorrect"
    
# Test requête GET authentifié
@hug.get('/api/token_authenticated', requires=token_key_authentication)
def token_auth_call(user: hug.directives.user):
    return '"Test requête GET ": You are user: {0}'.format(user['user'])

#--------------------------------------------------------------------------------------------

def toJson(data, model):
    model_fields = [column.name for column in model.__table__.columns]
    json = []

    print(model_fields)
    for dta in data:

        model = {}
        for fields in model_fields:
            model[fields] = getattr(dta, fields)
        json.append(model)

    return json


@hug.get('/api/models')
def models():
    models  = session.query(Models).all()
    json = toJson(models, Models)  
    return json
    

@hug.post('/api/model/create')
def createModel(body, response):
    name = body['name']
    file = body['file']

    # Chemin absolu du dossier où se trouve le fichier
    folder_path = os.path.abspath(os.path.join(os.getcwd(), 'AI model'))
    train_path  = os.path.abspath(os.path.join(os.getcwd(), 'AI model/' + name + '_train'))

    model_path = os.path.join(folder_path, name + '.h5')
    
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if os.path.isfile(model_path):
        response.status = falcon.get_http_status(403)
        return 'Impossible d\'importer un modèle qui à le même nom qu\'un autre!'
        
            # Vérifie si le dossier existe, sinon le crée
    with open(model_path, 'wb') as f:
        f.write(file)

    print('fichier créer')
    if not os.path.exists(train_path):
        print('dossier d\'entrainement créer')
        os.makedirs(train_path)

    model = Models(name=name, location=model_path)   
    session.add(model)
    session.commit()
    session.close() 
    try: 
        session.add(model)
        session.commit()
        session.close()  
    except:
        response.status = falcon.get_http_status(403)
        return 'Une erreur est survenue lors de l\'import du modèle, veuillez réesayer pluss tard'


    return 'Modèle enregistrer avec succès'


@hug.get('/api/classes')
def Classes():
    return [
        {'name': 'Tacos',     'nb_img': 1000, 'id': 1},
        {'name': 'Hamburger', 'nb_img': 1000, 'id': 2},
        {'name': 'Pizza',     'nb_img': 1000, 'id': 3}
    ]


@hug.post('/api/predict')
def predict(body, response):
    model_id = body['model_id']
    img      = body['img']

    model = session.query(Models).filter_by(id=model_id).first()
    
    # model = load_model(model.location)
    model.predict()
    return 'ok'