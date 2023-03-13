from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

from .classes import Classes
from .images import Images
class Predictions(Base):
    __tablename__ = 'predicitons'

    id            = Column(Integer, primary_key=True)
    user_feedback = Column(String)
    image_id      = mapped_column(ForeignKey('images.id'))
    classe_id     = mapped_column(ForeignKey('classes.id'))
    model_id      = mapped_column(ForeignKey("models.id"))  

    image = relationship(Images, backref='predicttions')
    classe = relationship(Classes, backref='predictions')