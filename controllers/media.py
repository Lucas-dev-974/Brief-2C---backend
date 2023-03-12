from database.entity import Images
from database.database import session
import hug 
import os

@hug.get('/{file_id}', output = hug.output_format.file)
# @hug.output_format()
def media(file_id: int):
    image = session.query(Images).filter_by(id=file_id).first()

    if not image:
        return 'Désoler l\'image n\'existe pas'
    
    base_path   = os.path.abspath('.')
    folder_path = os.path.join(base_path, 'images')
    file_path   = os.path.join(folder_path, image.location)
    
    return open(file_path, 'rb')