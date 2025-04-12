import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, DateTime
from sqlalchemy.orm import mapped_column

from src.db import Base


class BaseSchema(Base):
    __abstract__ = True

    id = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)