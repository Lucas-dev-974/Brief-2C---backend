import falcon
import hug

from database.entity   import Models, TrainedOn, Predictions, Classes
from database.database import session

from controllers.authentification import token_key_authentication

from utils import toJson, saveModelAsFile,loadImage, loadModel, getClasses, predictionIS, savePredictedImage, getClasseByClassename

# Donne la liste des models
@hug.get('/all')
def models():
    models  = session.query(Models).all()
    return toJson(models, Models) 

# Importation d'un modèle
@hug.post('/create', requires=token_key_authentication)
def create(body, response):
    name = body['name']
    file = body['file']
    classes = None

    # Récup des classes prédites
    if 'classes' in body:
        classes = body['classes'].split(',')

    saved = saveModelAsFile(file, name)

    if(saved['status'] == False):
        response.status = falcon.get_http_status(403)
        return saved['message']
    
    model = saved['model']

    if(classes != None and len(classes) > 1):
        for class_id in classes:
            trained_on = TrainedOn(model_id = model.id, classe_id=class_id)
            session.add(trained_on)
        session.commit()

    return 'Modèle enregistré avec succès'

@hug.post('/predict')
def predict(body):
    model_id = body['model_id']
    img      = body['img']
    filename = body['filename']
    image    = loadImage(img)

    _model     = session.query(Models).filter_by(id=model_id).first()
    trained_on = session.query(TrainedOn).filter_by(model_id=_model.id)
    trained_on = toJson(trained_on, TrainedOn)

    model      = loadModel(_model.location)
    trained_on = getClasses(trained_on)

    prediction =  model.predict(image)

    img_location = savePredictedImage(img, filename, 'predicted')

    
    predict = predictionIS(prediction[0], trained_on)

    classe = getClasseByClassename(predict['classe_name'])
    print(classe.id)
    preds = Predictions(img_location=img_location, id_trained_model=_model.id, classe = classe.id)

    session.add(preds)
    session.commit()
    result = {}
    result['prediction'] = predict['result']
    result['pred_id'] = preds.id
    return result

@hug.post('/feedback')
def feedbackPrediction(body):
    pred_id      = body['pred_id']
    categorie_id = body['categorie_id']

    prediction = session.query(Predictions).filter_by(id = pred_id).first()
    classe     = session.query(Classes).filter_by(id = categorie_id).first()

    prediction.user_feedback = classe.name
    session.flush()
    return 'ok'

# Récup des classes entrainé selon le modèle
@hug.get('/trained_on_classes/{model_id}', requires=token_key_authentication)
def trainedOnClasses(model_id: int):
    trained_on = session.query(TrainedOn).filter_by(model_id = model_id).all()
    trained_on = toJson(trained_on, TrainedOn)

    classes = []

    for classe in trained_on:
        entity = session.query(Classes).filter_by(id = classe['classe_id']).first()
        entity = { 'name': entity.name }
        classes.append(entity)

    return classes

# Test restrictions d'accès
# @hug.post('/test', requires=token_key_authentication)
# def test(request,body, user: hug.directives.user):
#     print(request.headers)
#     print("body=>",body['test'])
#     return user