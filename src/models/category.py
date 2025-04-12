from typing import TYPE_CHECKING

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.models.base import BaseSchema

if TYPE_CHECKING:
    from src.models.memory import Memory  # noqa: F401


class MemoryCategory(BaseSchema):
    __tablename__ = "memory_categories"

    name = Column(String, nullable=False)
    memories = relationship("Memory", back_populates="category")
