from entity.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class TrainedOn(Base):
    __tablename__ = 'trained_on'

    id        = Column(Integer, primary_key=True)
    id_classe = Column(Integer, ForeignKey('classes'))
    classe    = relationship('classes', cascade="all,delete")
    model_id  = Column(Integer, ForeignKey('trained_models.id'))
