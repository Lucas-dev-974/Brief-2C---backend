from .model import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class TrainedOn(Base):
    __tablename__ = 'trained_on'

    id        = Column(Integer, primary_key=True)
    id_classe = Column(Integer, ForeignKey('classes.id_classe'))
    model_id  = Column(Integer, ForeignKey('trained_models.id'))
