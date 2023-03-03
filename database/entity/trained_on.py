from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
class TrainedOn(Base):
    __tablename__ = 'trained_on'

    id        = Column(Integer, primary_key=True)
    classe_id = Column(Integer, ForeignKey('classes.id'))
    model_id  = Column(Integer, ForeignKey('models.id'))

    # classe = relationship('classes', backref='trained_on')