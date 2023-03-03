from .base import Base
from sqlalchemy import Column, Integer, String

class Classes(Base):
    __tablename__ = 'classes'

    id      = Column(Integer, primary_key=True)
    name    = Column(String, unique=True)
    location_folder = Column(String, unique=True)

    def __repr__(self) -> str:
        return f"Classes(id={self.id!r}, name={self.name!r}, location={self.location_folder!r})"    