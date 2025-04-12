from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.models.base import BaseSchema


class User(BaseSchema):
    __tablename__ = "users"

    name = Column(String, nullable=False)
    memories = relationship("Memory", back_populates="user")
