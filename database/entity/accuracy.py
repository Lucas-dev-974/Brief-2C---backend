from .base import Base
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Float, Boolean

# Contrainte unique à ajouter sur epoque et model_id
class Accuracy(Base):
    __tablename__ = "accuracy"

    id = Column(Integer, primary_key=True)
    epoque = Column(Integer)
    value = Column(Float)
    model_id = Column(Integer, ForeignKey('models.id'))
    validation = Column(Boolean)

    # À verif fonctionnement=>
    # UniqueConstraint('epoque','model_id')