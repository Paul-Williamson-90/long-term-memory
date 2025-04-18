import uuid
from datetime import datetime, timedelta
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import Memory, MemoryCategory, User


def create_memory(
    session: Session,
    text: str,
    embedding: list[float],
    user_id: Optional[uuid.UUID] = None,
    user: Optional[User] = None,
    category_id: Optional[uuid.UUID] = None,
    category: Optional[MemoryCategory] = None,
) -> Memory:
    """
    Create a new memory in the database.

    Args:
        session (Session): The SQLAlchemy session to use.
        text (str): The text of the memory.
        embedding (list[float]): The embedding of the memory.
        user_id (Optional[uuid.UUID]): The ID of the user associated with the memory.
        user (Optional[User]): The user associated with the memory.
        category_id (Optional[uuid.UUID]): The ID of the category associated with the memory.
        category (Optional[MemoryCategory]): The category associated with the memory.

    Returns:
        Memory: The created memory.
    """
    if not any([user_id, user]):
        raise ValueError("Either user_id or user must be provided.")
    if not any([category_id, category]):
        raise ValueError("Either category_id or category must be provided.")
    if all([user_id, user]):
        raise ValueError("Only one of user_id or user must be provided.")
    if all([category_id, category]):
        raise ValueError("Only one of category_id or category must be provided.")
    if user_id:
        user = session.query(User).filter(User.id == user_id).one_or_none()
        if user is None:
            raise ValueError(f"User with ID {user_id} not found.")
    if category_id:
        category = (
            session.query(MemoryCategory)
            .filter(MemoryCategory.id == category_id)
            .one_or_none()
        )
        if category is None:
            raise ValueError(f"Category with ID {category_id} not found.")

    memory = Memory(
        text=text,
        embedding=embedding,
        user=user,
        category=category,
    )
    session.add(memory)
    session.commit()
    session.refresh(memory)
    return memory


def get_memory_from_uuid(session: Session, uuid: uuid.UUID) -> Optional[Memory]:
    """
    Get a memory from the database by its UUID.

    Args:
        session (Session): The SQLAlchemy session to use.
        uuid (uuid.UUID): The UUID of the memory to retrieve.

    Returns:
        Optional[Memory]: The retrieved memory, or None if not found.
    """
    return (
        session.query(Memory)
        .join(MemoryCategory, Memory.category_id == MemoryCategory.id)
        .join(User, Memory.user_id == User.id)
        .filter(Memory.id == uuid)
        .one_or_none()
    )


class SearchMemoriesResult(BaseModel):
    memory: Memory
    score: float

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


def search_memories_by_vector(
    session: Session,
    query_embedding: list[float],
    user_id: uuid.UUID,
    category: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    top_k: int = 30,
    threshold: float = 0.6,
) -> list[SearchMemoriesResult]:
    """
    Search for memories in the database using a vector query.

    Args:
        session (Session): The SQLAlchemy session to use.
        query_embedding (list[float]): The embedding vector to search for.
        user_id (uuid.UUID): The ID of the user associated with the memories.
        category (Optional[str]): The category to filter memories by.
        date_from (Optional[datetime]): The start date to filter memories by.
        date_to (Optional[datetime]): The end date to filter memories by.
        top_k (int): The number of top results to return.
        threshold (float): The threshold for cosine distance.

    Returns:
        list[dict]: A list of dictionaries, where each dictionary contains the memory and its associated score.
    """
    if not date_from:
        date_from = datetime(1970, 1, 1)
    if not date_to:
        date_to = datetime.now() + timedelta(days=1)
    query = select(
        Memory, Memory.embedding.cosine_distance(query_embedding).label("score")
    )
    if category:
        query = query.filter(
            Memory.embedding.cosine_distance(query_embedding) < threshold,
            Memory.user_id == user_id,
            Memory.category.has(name=category),
            Memory.created_at.between(date_from, date_to),
        )
    else:
        query = query.filter(
            Memory.embedding.cosine_distance(query_embedding) < threshold,
            Memory.user_id == user_id,
            Memory.created_at.between(date_from, date_to),
        )

    query = query.order_by(Memory.embedding.cosine_distance(query_embedding)).limit(
        top_k
    )
    results = session.execute(query).all()

    return [
        SearchMemoriesResult(memory=result[0], score=result[1]) for result in results
    ]
