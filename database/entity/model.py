from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import Column, Integer, String
from .base import Base
from typing import List

from .trained_on import TrainedOn
from .prediction import Predictions

class Models(Base):
    __tablename__ = 'models'

    id      = Column(Integer, primary_key=True) 
    name    = Column(String, unique=True)
    location= Column(String, unique=True)

    trained_on_classes = relationship(TrainedOn, backref='models')  
    predictions        = relationship(Predictions, backref='models')

