from .model import Base
from sqlalchemy import Column, Integer, String

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(40), unique=True)
    email= Column(String(70), unique=True)
    password = Column(String(300))

    def __repr__(self) -> str:
        return f"Users(id={self.id!r}, name={self.name!r}, location={self.location!r})"