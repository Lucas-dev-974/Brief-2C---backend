from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String
from .model import Base

class Models(Base):
    __tablename__ = 'models'

    id      = Column(Integer, primary_key=True)
    name    = Column(String, unique=True)
    location= Column(String, unique=True)
    train   = relationship('trained_models', cascade="all,delete")
    
    # def __repr__(self) -> str:
    #     return f"Models(id={self.id!r}, name={self.name!r}, location={self.location!r})"    