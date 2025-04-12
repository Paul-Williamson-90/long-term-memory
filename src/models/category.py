from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.models.base import BaseSchema


class MemoryCategory(BaseSchema):
    __tablename__ = "memory_categories"

    name = Column(String, nullable=False)
    memories = relationship("Memory", back_populates="category")
