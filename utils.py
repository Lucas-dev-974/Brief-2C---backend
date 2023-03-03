from joblib import load
from PIL import Image
import numpy as np

import os
import io

from database.database import session
from database.entity   import Models, Classes

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

    print(model_fields)
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

    filename = datetime.datetime.fromtimestamp(time.time()).strftime('%H%M%S') + filename

    if(clas == 'predicted'):
        save_path = os.path.join(save_path, 'predicted')
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
            
    return f'L\'image est de la classe {classes[index]} à {round(pred_percent * 100,2)}%'