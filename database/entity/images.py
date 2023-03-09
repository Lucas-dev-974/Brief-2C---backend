from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Images(Base):
    __tablename__ = 'images'

    id         = Column(Integer, primary_key=True)
    location   = Column(String)  # folder/filename.ext
    classe     = Column(Integer, ForeignKey('classes.id'), nullable=True) 
   