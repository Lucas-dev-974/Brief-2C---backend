from database.database import session
from database.entity import  Classes
from utils import toJson
from controllers.authentification import token_key_authentication

import hug

@hug.get('/all', requires=token_key_authentication)
def getClasses():
    classes  = session.query(Classes).all()
    return toJson(classes, Classes)
