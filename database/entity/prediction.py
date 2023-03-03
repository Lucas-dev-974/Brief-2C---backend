from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Predictions(Base):
    __tablename__ = 'predicitons'

    id               = Column(Integer, primary_key=True)
    user_feedback    = Column(String)
    img_location     = Column(String)

    id_trained_model = Column(Integer, ForeignKey('models.id'))
    classe           = Column(Integer, ForeignKey('classes.id'))