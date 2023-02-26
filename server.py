import hug
from hug.middleware import CORSMiddleware
# from keras.models import load_model
from database.entity import Models
import os 
import falcon


from database.database import session

api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api))

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
