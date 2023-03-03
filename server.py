from hug.middleware import CORSMiddleware
from controllers import model, classe
import hug


api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api))

api.extend(model, '/api/model')
api.extend(classe, '/api/classe')