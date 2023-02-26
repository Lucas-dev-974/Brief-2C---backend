from .model import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class TrainedModel(Base):
    __tablename__ = 'trained_models'

    id          = Column(Integer, primary_key=True)
    nb_class    = Column(Integer)
    total_img   = Column(Integer)
    trained_location= Column(String, unique=True)
    
    model_id    = Column(Integer, ForeignKey('models.id'))
    
    # on_classes  = relationship('trained_on')
    # predictions = relationship('predictions')