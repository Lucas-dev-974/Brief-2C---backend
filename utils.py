from database.entity   import Models, Classes, Images
from database.database import session
from joblib import load
from PIL    import Image
import numpy as np

import os
import io




def img_to_array(img, data_format=None, dtype=None):
    x = np.asarray(img, dtype=dtype)
    if len(x.shape) == 3:
        if data_format == "channels_first":
            x = x.transpose(2, 0, 1)
    elif len(x.shape) == 2:
        if data_format == "channels_first":
            x = x.reshape((1, x.shape[0], x.shape[1]))
        else:
            x = x.reshape((x.shape[0], x.shape[1], 1))
    else:
        raise ValueError(f"Unsupported image shape: {x.shape}")
    return x


def init_img(img):
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0
    return img_array

def loadImage(img):
    image = Image.open(io.BytesIO(img))
    image = image.resize((224, 224))    
    return init_img(image)

def loadModel(location):
    return load(location)

def toJson(data, model):
    model_fields = [column.name for column in model.__table__.columns]
    json = []

    for dta in data:
        model = {}
        for fields in model_fields:
            model[fields] = getattr(dta, fields)
        json.append(model)

    return json


def saveModelAsFile(file, name):
    folder_path = os.path.abspath(os.path.join(os.getcwd(), 'ai_models'))
    train_path  = os.path.abspath(os.path.join(os.getcwd(), 'ai_models/' + name + '_train'))
    model_path  = os.path.join(folder_path, name + '.model')

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if os.path.isfile(model_path):
        state = {}
        state['status'] = False
        state['message'] =  'Impossible d\'importer un modèle qui à le même nom qu\'un autre!'
        return state
        
            # Vérifie si le dossier existe, sinon le crée
    with open(model_path, 'wb') as f:
        f.write(file)

    if not os.path.exists(train_path):
        os.makedirs(train_path)

    
    model = Models(name=name, location=model_path)   
    session.add(model)
    session.commit()
    # os.close()
    return {'status': True, 'model': model}


import time
import datetime
def savePredictedImage(file, filename, clas):
    save_path = os.path.abspath(os.path.join(os.getcwd(), 'images'))
    file_path = ''
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    filename = datetime.datetime.fromtimestamp(time.time()).strftime('%H%M%S') + filename


    if(clas == 'predicted'):
        save_path = os.path.join(save_path, 'predicted')
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        file_path = os.path.join(save_path, filename)
    
        with open(file_path, 'wb') as f:
            f.write(file)

    return file_path

def getClasses(trainedon):
    classes = []
    for trained_on in trainedon:
        print(trained_on)
        classe = session.query(Classes).filter_by(id = trained_on['classe_id']).first()
        print('classe: -- ', classe)
        classes.append(classe.name)
    return sorted(classes)

def predictionIS(preds, classes):
    pred_percent = 0
    index = 0

    for idx, pred in enumerate(preds):
        if pred > pred_percent:
            pred_percent = pred
            index = idx
            
    result = {}
    result['result']      = f'L\'image est de la classe {classes[index]} à {round(pred_percent * 100,2)}%'
    result['classe_name'] = classes[index]

    return result


def getClasseByClassename(name):
    return session.query(Classes).filter_by(name = name).first()


import json
from sqlalchemy.orm import class_mapper
def Serializer(query):
    # Créer une liste de dictionnaires pour les résultats sérialisés
    serialized_results = []
    for r in query:
        # Accéder aux propriétés de chaque relation et les inclure dans le dictionnaire
        serialized_result = {}
        for prop in class_mapper(r.__class__).iterate_properties:
            if hasattr(r, prop.key):
                if prop.key != 'password': # Exclure la propriété "password" pour des raisons de sécurité
                    val = getattr(r, prop.key)
                    if prop.uselist:
                        print('serialized_result', prop.key)
                        serialized_result[prop.key] = [dict(p) for p in val]
                    else:
                        serialized_result[prop.key] = dict(val)
        serialized_results.append(serialized_result)

    # Sérialiser les résultats en JSON
    serialized_results_json = json.dumps(serialized_results)
    return serialized_results_json