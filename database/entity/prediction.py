from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship

class Predictions(Base):
    __tablename__ = 'predicitons'

    id            = Column(Integer, primary_key=True)
    user_feedback = Column(String)
    img_location  = Column(String)
    classe_id     = mapped_column(ForeignKey('classes.id'))
    model_id      = mapped_column(ForeignKey("models.id"))

    # model  = relationship("models",  back_populates="predictions")
    # classe = relationship('classes', back_populates='classes')