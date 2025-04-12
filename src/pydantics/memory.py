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
    user_id: uuid.UUID
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
    def from_dbo(cls, dbo: Memory, score: Optional[float] = None) -> "SemanticMemory":
        return cls(
            id=dbo.id,
            text=dbo.text,
            text_embedding=dbo.embedding,
            category=dbo.category.name,
            user_id=dbo.user.id,
            score=score,
            created_at=dbo.created_at,
        )

    def _embed_text(self) -> None:
        if self.text_embedding is None:
            self.text_embedding = get_text_embedding([self.text])[0]

    def save(self, session: Session) -> Memory:
        self._embed_text()
        if self.text_embedding is None:
            raise ValueError("Text embedding must be provided.")
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
        if self.id is None:
            raise ValueError("Memory ID must be provided.")
        memory = get_memory_from_uuid(session, self.id)
        if memory is None:
            raise ValueError(f"Memory with ID {self.id} not found.")
        session.delete(memory)
        session.commit()


class MemorySearchResults(BaseModel):
    memories: list[SemanticMemory]

    # @model_validator(mode="after")
    # def memory_sort_by_score(self) -> "MemorySearchResults":
    #     scored_memories = [m for m in self.memories if m.score is not None]
    #     non_scored_memories = [m for m in self.memories if m.score is None]
    #     scored_memories.sort(key=lambda x: x.score, reverse=True)
    #     self.memories = scored_memories + non_scored_memories
    #     return self

    @model_validator(mode="after")
    def memory_sort_by_created_date(self) -> "MemorySearchResults":
        dated_memories = [
            m for m in self.memories if isinstance(m.created_at, datetime)
        ]
        non_dated_memories = [
            m for m in self.memories if not isinstance(m.created_at, datetime)
        ]
        dated_memories.sort(key=lambda x: x.created_at, reverse=True)  # type: ignore
        self.memories = dated_memories + non_dated_memories
        return self
