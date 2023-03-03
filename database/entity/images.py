from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Images(Base):
    __tablename__ = 'images'

    id         = Column(Integer, primary_key=True)
    location   = Column(String)
    classe  = Column(Integer, ForeignKey('classes.id'))
   