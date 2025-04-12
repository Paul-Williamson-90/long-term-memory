from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.orm import mapped_column, relationship

from src.models.base import BaseSchema


class Memory(BaseSchema):
    __tablename__ = "memories"

    text = Column(String, nullable=False)
    embedding = Column(Float, nullable=False)

    category_id = mapped_column(ForeignKey("memory_categories.id"))
    category = relationship("Category", back_populates="memories")

    user_id = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="memories")
