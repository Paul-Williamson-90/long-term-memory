import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, model_validator
from sqlalchemy.orm import Session

from src.embedding import get_text_embedding
from src.models import Memory
from src.queries import (
    create_memory,
    get_memory_from_uuid,
    get_or_create_category_by_name,
)


class SemanticMemory(BaseModel):
    id: Optional[uuid.UUID] = None
    text: str
    text_embedding: Optional[list[float]] = None
    category: str
    user_id: str
    created_at: Optional[datetime] = None
    score: Optional[float] = None

    def __str__(self) -> str:
        if self.created_at:
            date_str = self.created_at.strftime("%d %B %Y")
            return f"Memory From {date_str}\n```\n{self.text}\n```"
        else:
            return self.text

    @classmethod
    def from_memory_uuid(cls, session: Session, id: uuid.UUID) -> "SemanticMemory":
        memory = get_memory_from_uuid(session, id)
        if memory is None:
            raise ValueError(f"Memory with ID {id} not found.")
        return cls(
            id=memory.id,
            text=memory.text,
            text_embedding=memory.embedding,
            category=memory.category.name,
            user_id=memory.user.id,
            created_at=memory.created_at,
        )

    @classmethod
    def from_dbo(cls, dbo: Memory) -> "SemanticMemory":
        return cls(
            id=dbo.id,
            text=dbo.text,
            text_embedding=dbo.embedding,
            category=dbo.category.name,
            user_id=dbo.user.id,
        )

    def _embed_text(self) -> None:
        if self.text_embedding is None:
            self.text_embedding = get_text_embedding(self.text)[0]

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

    def delete(self, session: Session) -> None:
        memory = get_memory_from_uuid(session, self.id)
        if memory is None:
            raise ValueError(f"Memory with ID {self.id} not found.")
        session.delete(memory)
        session.commit()


class MemorySearchResults(BaseModel):
    memories: list[SemanticMemory]

    @model_validator(mode="after")
    def memory_sort_by_score(self) -> "MemorySearchResults":
        self.memories.sort(key=lambda x: x.score, reverse=True)
        return self
