import hug
from hug.middleware import CORSMiddleware
import logging

logging.basicConfig(level=logging.DEBUG)

api = hug.API(__name__)
api.http.add_middleware(CORSMiddleware(api))

@hug.get('/api/models')
def Models():
    print('ok')
    logging.debug('ok')
    return [
        {'name': 'Xception', 'id': 1},
        {'name': 'Mobilnet', 'id': 2},
        {'name': 'Vgg16', 'id': 3}
    ]   


@hug.get('/api/classes')
def Classes():
    return [
        {'name': 'Tacos', 'nb_img': 1000, 'id': 1},
        {'name': 'Hamburger', 'nb_img': 1000, 'id': 2},
        {'name': 'Pizza', 'nb_img': 1000, 'id': 3}
    ]

# @hug.get('/api/models')
# def Models():
#     return [
#         {'name': 'Xception', 'id': 1},
#         {'name': 'Mobilnet', 'id': 2},
#         {'name': 'Vgg16', 'id': 3}
#     ]