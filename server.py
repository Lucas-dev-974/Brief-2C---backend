from controllers import authentification, model, classe, stats_globales, media
from hug.middleware import CORSMiddleware
import hug

api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api, allow_origins=['*'])) # allow_origins à restreindre pour le déploiement

api.extend(model, '/api/model')
api.extend(classe, '/api/classe')
api.extend(authentification, '/api/authentication')
api.extend(stats_globales, '/api/stats_globales')
api.extend(media, '/api/media')