import falcon
import hug

from database.entity   import Models, TrainedOn, Predictions, Classes
from database.database import session

from utils import toJson, saveModelAsFile,loadImage, loadModel, getClasses, predictionIS, savePredictedImage

@hug.get('/all')
def models():
    models  = session.query(Models).all()
    return toJson(models, Models) 

@hug.post('/create')
def create(body, response):
    name = body['name']
    file = body['file']
    classes = None

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

    return 'Modèle enregistrer avec succès'



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
    preds = Predictions(img_location=img_location, id_trained_model=_model.id)

    session.add(preds)
    session.commit()
    
    predict = predictionIS(prediction[0], trained_on)
    
    result = {}
    result['prediction'] = predict
    result['model'] = _model.id
    return result

@hug.post('/feedback')
def feedbackPrediction(body):
    pred_id      = body['model']
    categorie_id = body['categorie']

    prediction = session.query(Predictions).filter_by(id = pred_id).first()
    classe     = session.query(Classes).filter_by(id = categorie_id).first()

    prediction.user_feedback = classe.name

    session.flush()


    return 'ok'