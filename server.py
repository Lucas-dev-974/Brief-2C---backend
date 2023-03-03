from hug.middleware import CORSMiddleware
import hug
import jwt
from database.database import session
from controllers import authentification, model, classe

api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api, allow_origins=['*'])) # allow_origins à restreindre pour le déploiement

api.extend(model, '/api/model')
api.extend(classe, '/api/classe')
api.extend(authentification, '/api/authentication')