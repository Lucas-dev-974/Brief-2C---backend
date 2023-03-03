from database.database import session
from database.entity import  Classes
from utils import toJson

import hug

@hug.get('/all')
def getClasses():
    classes  = session.query(Classes).all()
    return toJson(classes, Classes)
