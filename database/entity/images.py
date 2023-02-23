from entity.model import Base
from sqlalchemy import Column, Integer, String, ForeignKey

class Images(Base):
    __tablename__ = 'images'

    id         = Column(Integer, primary_key=True)
    location   = Column(String)
    id_classe  = Column(Integer, ForeignKey('classes.id_classe'))
   