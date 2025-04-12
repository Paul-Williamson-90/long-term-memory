from typing import Optional

from sqlalchemy.orm import Session

from src.models import MemoryCategory


def create_category(session: Session, name: str) -> MemoryCategory:
    """
    Create a new category in the database.

    Args:
        session (Session): The SQLAlchemy session to use.
        name (str): The name of the category.

    Returns:
        MemoryCategory: The created category.
    """
    category = MemoryCategory(name=name)
    session.add(category)
    session.commit()
    session.refresh(category)
    return category


def get_category_by_name(session: Session, name: str) -> Optional[MemoryCategory]:
    """
    Get a category by its name.

    Args:
        session (Session): The SQLAlchemy session to use.
        name (str): The name of the category.

    Returns:
        Optional[MemoryCategory]: The category with the specified name.
    """
    return session.query(MemoryCategory).filter(MemoryCategory.name == name).one_or_none()


def get_or_create_category_by_name(
    session: Session, name: str
) -> MemoryCategory:
    """
    Get or create a category by its name.

    Args:
        session (Session): The SQLAlchemy session to use.
        name (str): The name of the category.

    Returns:
        MemoryCategory: The category with the specified name.
    """
    category = get_category_by_name(session, name)
    if category is None:
        category = create_category(session, name)
    return category