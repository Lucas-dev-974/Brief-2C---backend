from entity.model import Base
# from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import Column, Integer, String

class Models(Base):
    __tablename__ = 'models'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    location= Column(String, unique=True)

    def __repr__(self) -> str:
        return f"Models(id={self.id!r}, name={self.name!r}, location={self.location!r})"    