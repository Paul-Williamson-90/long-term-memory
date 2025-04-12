import uuid
from typing import Optional

from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.embedding import get_text_embedding
from src.models import Memory
from src.queries import (
    create_memory,
    get_memory_from_uuid,
    get_or_create_category_by_name,
)


class SemanticMemory(BaseModel):
    text: str
    text_embedding: Optional[list[float]] = None
    category: str
    user_id: str

    @classmethod
    def from_memory_uuid(cls, session: Session, id: uuid.UUID) -> "SemanticMemory":
        memory = get_memory_from_uuid(session, id)
        if memory is None:
            raise ValueError(f"Memory with ID {id} not found.")
        return cls(
            text=memory.text,
            text_embedding=memory.embedding,
            category=memory.category.name,
            user_id=memory.user.id,
        )

    @classmethod
    def from_dbo(cls, dbo: Memory) -> "SemanticMemory":
        return cls(
            text=dbo.text,
            text_embedding=dbo.embedding,
            category=dbo.category.name,
            user_id=dbo.user.id,
        )

    def _embed_text(self) -> None:
        if self.text_embedding is None:
            self.text_embedding = get_text_embedding(self.text)[0]

    def to_dbo(self) -> Memory:
        self._embed_text()
        return Memory(
            text=self.text,
            embedding=self.text_embedding,
            category=self.category,
            user_id=self.user_id,
        )

    def save(self, session: Session) -> Memory:
        self._embed_text()
        category = get_or_create_category_by_name(session, self.category)
        memory = create_memory(
            session,
            text=self.text,
            embedding=self.text_embedding,
            user_id=self.user_id,
            category=category,
        )
        return memory
