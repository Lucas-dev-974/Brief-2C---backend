import hug
from hug.middleware import CORSMiddleware

api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api))

@hug.get('/api/models')
def Models():
    return 'true'   


@hug.get('/api/classes')
def Classes():
    return [
        {'name': 'Tacos', 'nb_img': 1000, 'id': 1},
        {'name': 'Hamburger', 'nb_img': 1000, 'id': 2},
        {'name': 'Pizza', 'nb_img': 1000, 'id': 3}
    ]

@hug.get('/api/models')
def Models():
    return [
        {'name': 'xception', 'id': 1},
        {'name': 'mobilnet', 'id': 2},
        {'name': 'vgg16', 'id': 3}
    ]