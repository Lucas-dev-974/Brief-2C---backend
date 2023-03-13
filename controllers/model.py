import falcon
import hug

from database.entity   import Models, TrainedOn, Predictions, Classes, Images
from database.database import session

from database.entity.loss import Loss
from database.entity.accuracy import Accuracy

from controllers.authentification import token_key_authentication
import os
from utils import loadMD, makePrediction, getModelTrainClasses, toJson, saveModelAsFile,loadImage, loadModel, getClasses, predictionIS, savePredictedImage, getClasseByClassename, validator

# Donne la liste des models
@hug.get('/all')
def models():
    return toJson(session.query(Models).all(), Models)

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
def predict(body: dict):
    # Vérification si les champs requis sont bien dans la requête
    if not validator(body, ['model_id', 'img', 'filename']):
        return 'Veuillez renseigner les champs id model, image et nom de l\'image'
    
    # Récupèrage des paramètre de requis
    model_id = body['model_id']
    img      = body['img']
    filename = body['filename']
    image    = loadImage(img)
    
    # Récuprère l'entité du model puis le modèle charger et les classes d'entrainement du modèle
    _model, model, classes = loadMD(model_id)
    
    # Execute la prédiction sur l'image donner et enregistre l'image sur le serveur et dans la BDD -> + sauvegarde de la prédiction puis retourne la prediction et son entité
    predict, preds = makePrediction(model, _model, image, img, filename, classes)

    return { "prediction": predict['result'], 'pred_id':    preds.id }

@hug.post('/feedback')
def feedbackPrediction(body):
    # Vérification si les champs requis sont bien dans la requête
    if not validator(body, ['pred_id', 'categorie_id']):
        return 'Veuillez renseigner les champs id de la prediciton et id de la bonne classe'
    
    # Récupèrage des paramètre de requis
    pred_id      = body['pred_id']
    categorie_id = body['categorie_id']

    # Récuperation de la prediction et de la classe via leurs ID
    prediction = session.query(Predictions).filter_by(id = pred_id).first()
    classe     = session.query(Classes).filter_by(id = categorie_id).first()

    # Si la classe n'existe pas alors retourne une erreur 
    if not classe:
        return 'Désoler la classe n\'existe pas !'
    
    # Mise à jour de la prediction en BDD 
    prediction.user_feedback = classe.name
    session.flush()
    session.commit()
    return 'Prediction mis à jour'

# Récup des classes entrainé selon le modèle
@hug.get('/trained_on_classes/{model_id}')
def trainedOnClasses(model_id: int):
    classes = getModelTrainClasses(model_id)
    print(classes)
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

@hug.get('/pieData/{model_id}', requires=token_key_authentication)
def recupPieData(model_id:int):

    # Récup data depuis la BDD
    nbBonnesPred = session.query(Predictions).where(Predictions.model_id == model_id).where(Predictions.user_feedback == None).count()
    nbMauvaisesPred = session.query(Predictions).where(Predictions.model_id == model_id).where(Predictions.user_feedback != None).count()

    return { 'nbMauvaisesPred' : nbMauvaisesPred, 'nbBonnesPred' : nbBonnesPred }


@hug.get('/bad_predictions/{model_id}')
def badPredictions(model_id: int):
    predictions = session.query(Predictions).where(Predictions.model_id == model_id, Predictions.user_feedback != None).join(Classes).all()
    jsoned = toJson(predictions, Predictions)

    for json in jsoned:
        json['classe'] = predictions[0].classe.name
        
    print(jsoned)
    return jsoned


