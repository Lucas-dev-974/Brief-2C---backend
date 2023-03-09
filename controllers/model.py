import falcon
import hug

from database.entity   import Models, TrainedOn, Predictions, Classes
from database.database import session

from database.entity.loss import Loss
from database.entity.accuracy import Accuracy

from controllers.authentification import token_key_authentication

from utils import toJson, saveModelAsFile,loadImage, loadModel, getClasses, predictionIS, savePredictedImage, getClasseByClassename, Serializer

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
    
    preds  = Predictions(img_location=img_location, model_id=_model.id, classe_id=classe.id)

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
    session.commit()
    return 'ok'

# import json
# @hug.get('/trained_on_classes/{model_id}')
# def trainedOnClasses(model_id: int):
#     trainedon  = session.query(Models).where(Models.id == model_id).join(TrainedOn).values()
#     print('trainedon', trainedon)
#     trained = Serializer(trainedon)
    
#     print(trained)

#     trained_on = session.query(TrainedOn).filter_by(model_id = model_id).all()
#     trained_on = toJson(trained_on, TrainedOn)

#     classes = []

#     for classe in trained_on:
#         entity = session.query(Classes).filter_by(id = classe['classe_id']).first()
#         entity = { 'name': entity.name }
#         classes.append(entity)

#     return classes


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

    # return trained_on
    return classes

# Récup des metrics
@hug.get('/metrics/{model_id}', requires=token_key_authentication)
def recupMetrics(model_id: int):
    
    # Récup des metrics depuis BDD
    test_loss = session.query(Loss).where(Loss.validation==False and Loss.model_id == model_id).values(Loss.value)
    val_loss = session.query(Loss).where(Loss.validation == True and Loss.model_id == model_id).values(Loss.value)
    test_accuracy = session.query(Accuracy).where(Accuracy.validation == False and Accuracy.model_id == model_id).values(Accuracy.value)
    val_accuracy = session.query(Accuracy).where(Accuracy.validation == True and Accuracy.model_id == model_id).values(Accuracy.value)

    return {"test_loss": test_loss, "test_accuracy": test_accuracy, "val_loss": val_loss, "val_accuracy": val_accuracy}


@hug.get('/bad_predictions')
def badPredictions(model_id: int):
    predictions = session.query(Predictions).where(Predictions.model_id == model_id, Predictions.user_feedback != None).all()
    jsoned = toJson(predictions, Predictions)
    print(jsoned)
    return jsoned