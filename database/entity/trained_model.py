from entity.model import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class TrainedModel(Base):
    __tablename__ = 'trained_models'

    id          = Column(Integer, primary_key=True)
    nb_class    = Column(Integer)
    trained_location= Column(String, unique=True)
    total_img = Column(Integer)
    model_id  = Column(Integer, ForeignKey('models.id'))
    
    def __repr__(self) -> str:
        return f"TrainedModel(id={self.id!r}, nb_class={self.nb_class!r}, totalImg={self.total_img!r}, modelID{self.model_id})"    
    