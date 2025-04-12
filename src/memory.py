import uuid
from typing import Optional

from src.db import get_session
from src.embedding import get_query_embedding
from src.pydantics import MemorySearchResults, SemanticMemory
from src.queries import create_user, get_user_by_name, search_memories_by_vector


class MemoryInterface:
    def search(
        self,
        query: str,
        user_id: uuid.UUID,
        category: Optional[str] = None,
        top_k: int = 30,
        threshold: float = 0.6,
    ) -> MemorySearchResults:
        if not any([query, user_id]):
            raise ValueError("Query and user_id must be provided.")
        query_embedding = get_query_embedding(query)
        with get_session() as session:
            results = search_memories_by_vector(
                session, query_embedding, user_id, category, top_k, threshold
            )
            if results:
                memories = MemorySearchResults(
                    memories=[
                        SemanticMemory.from_dbo(m["memory"], m["score"])  # type: ignore
                        for m in results
                    ],
                )
                return memories
            else:
                return MemorySearchResults(memories=[])

    def add_memory(
        self, text: str, category: str, user_id: uuid.UUID
    ) -> SemanticMemory:
        if not any([text, category, user_id]):
            raise ValueError("Text, category, and user_id must be provided.")
        with get_session() as session:
            memory = SemanticMemory(text=text, category=category, user_id=user_id)
            memory.save(session)
        return memory

    def remove_memory_by_uuid(self, memory_id: uuid.UUID) -> bool:
        if not memory_id:
            raise ValueError("Memory ID must be provided.")
        with get_session() as session:
            memory = SemanticMemory.from_memory_uuid(session, memory_id)
            if memory:
                memory.delete(session)
                return True
            else:
                raise ValueError(f"Memory with ID {memory_id} not found.")
        return False

    def create_user(self, name: str) -> uuid.UUID:
        if not name:
            raise ValueError("Name must be provided.")
        with get_session() as session:
            user = create_user(session, name)
            user_id = user.id
        return user_id

    def find_user(self, name: str) -> Optional[uuid.UUID]:
        if not name:
            raise ValueError("Name must be provided.")
        with get_session() as session:
            user = get_user_by_name(session, name)
            if not user:
                return None
            user_id = user.id
        return user_id
