from typing import TYPE_CHECKING

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.models.base import BaseSchema

if TYPE_CHECKING:
    from src.models.memory import Memory  # noqa: F401


class User(BaseSchema):
    __tablename__ = "users"

    name = Column(String, nullable=False, unique=True)
    memories = relationship("Memory", back_populates="user")
