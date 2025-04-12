from typing import Optional

from sqlalchemy.orm import Session

from src.models import User


def create_user(session: Session, name: str) -> User:
    """
    Create a new user in the database.

    Args:
        session (Session): The SQLAlchemy session to use.
        name (str): The name of the user.

    Returns:
        User: The created user.
    """
    user = User(name=name)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


def get_user_by_name(session: Session, name: str) -> Optional[User]:
    """
    Get a user by name from the database.

    Args:
        session (Session): The SQLAlchemy session to use.
        name (str): The name of the user.

    Returns:
        Optional[User]: The user with the specified name.
    """
    user = session.query(User).filter(User.name == name).one_or_none()
    return user