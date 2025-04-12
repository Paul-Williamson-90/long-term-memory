from typing import TYPE_CHECKING

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship

from src.models.base import BaseSchema
from src.settings import settings

if TYPE_CHECKING:
    from src.models.category import MemoryCategory  # noqa: F401
    from src.models.user import User  # noqa: F401


class Memory(BaseSchema):
    __tablename__ = "memories"

    text = Column(String, nullable=False)
    embedding = Column(Vector(settings.embedding_model_dims), nullable=False)

    category_id = mapped_column(ForeignKey("memory_categories.id"))
    category = relationship("MemoryCategory", back_populates="memories")

    user_id = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="memories")
