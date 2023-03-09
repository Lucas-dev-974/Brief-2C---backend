from .base import Base
from sqlalchemy import Column, Integer,  ForeignKey
from sqlalchemy.orm import relationship, mapped_column

from .classes import Classes

class TrainedOn(Base):
    __tablename__ = 'trained_on'

    id        = Column(Integer, primary_key=True)
    classe_id = mapped_column(ForeignKey('classes.id'))
    model_id  = mapped_column(ForeignKey('models.id'))

    classe = relationship(Classes, backref='trained_on')
    # model  = relationship('models',  back_populates='trained_on')
