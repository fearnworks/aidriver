"""
This module defines several utility functions and classes that are used as dependencies in FastAPI routes. These dependencies can be used to manage database sessions, authenticate users, and manage user permissions.

Dependencies:
    get_db(): Manages database sessions using a SQLAlchemy SessionLocal instance. It is used as a dependency in FastAPI routes to provide a session for database operations.

    get_example_client():Stub for wherever client operations are required.

    get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)): Authenticates a user using a JWT token and retrieves the user's information from the database. Used as a dependency in routes that require user authentication.

    get_current_active_superuser(current_user: User = Depends(get_current_user)): Checks if the authenticated user is a superuser. Used as a dependency in routes that require superuser privileges.

Models:
    TokenData: Pydantic model for handling token data.

"""

from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlalchemy.orm.session import Session
from ai_driver.server import crud
from ai_driver.server.core.auth import oauth2_scheme
from ai_driver.server.core.config import settings
from ai_driver.server.db.session import SessionLocal
from ai_driver.server.models.user import User


class TokenData(BaseModel):
    username: Optional[str] = None


def get_db() -> Generator:
    """
    Dependency for getting a database session.
    This function creates an instance of SessionLocal that provides a session for database operations.
    The session is closed after it is used.

    Returns:
        A SQLAlchemy SessionLocal instance.
    """

    db: Session = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()


def get_current_user(db=Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """
    This function decodes the JWT token to get the username and then retrieves the user's information
    from the database.

    Args:
        db: A SQLAlchemy Session.
        token: A JWT token.

    Raises:
        HTTPException: If the token is invalid or the user is not found in the database.

    Returns:
        The authenticated User.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            settings.auth.JWT_SECRET,
            algorithms=[settings.auth.ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    This function checks if the authenticated user is a superuser.

    Args:
        current_user: The authenticated User.

    Raises:
        HTTPException: If the user is not a superuser.

    Returns:
        The authenticated User if they are a superuser.
    """
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
