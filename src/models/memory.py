from sqlalchemy import Column, String, ForeignKey, Float
from sqlalchemy.orm import relationship, mapped_column

from src.models.base import BaseSchema


class Memory(BaseSchema):
    __tablename__ = 'memories'
    
    text = Column(String, nullable=False)
    embedding = Column(Float, nullable=False)
    
    category_id = mapped_column(ForeignKey("memory_categories.id"))
    category = relationship('Category', back_populates='memories')
    
    user_id = mapped_column(ForeignKey("users.id"))
    user = relationship('User', back_populates='memories')