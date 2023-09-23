"""
This module provides the functionality for user authentication and token management. It includes
functions for user authentication, and creation of access tokens.
"""

from datetime import datetime, timedelta
from typing import List, MutableMapping, Optional, Union

from ai_driver.server.core.config import settings
from ai_driver.server.core.security import verify_password
from ai_driver.server.models.user import User
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm.session import Session

JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]

# Define OAuth2 password bearer with a token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def authenticate(
    *,
    email: str,
    password: str,
    db: Session,
) -> Optional[User]:
    """
    Verifies the email and password to authenticate a user.

    Args:
        email (str): The email of the user.
        password (str): The password of the user.
        db (Session): The database session.

    Returns:
        Optional[User]: The authenticated user if authentication is successful, otherwise None.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(*, sub: str) -> str:
    """
    Creates an access token for a user.

    Args:
        sub (str): The subject for which the token is issued, typically the user ID.

    Returns:
        str: The generated access token.
    """
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.auth.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
) -> str:
    """
    Helper function to create a token with a specific type and lifetime.

    Args:
        token_type (str): The type of the token.
        lifetime (timedelta): The lifetime of the token.
        sub (str): The subject for which the token is issued, typically the user ID.

    Returns:
        str: The generated token.
    """
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type

    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    # The "exp" (expiration time) claim identifies the expiration time on
    # or after which the JWT MUST NOT be accepted for processing
    payload["exp"] = expire

    # The "iat" (issued at) claim identifies the time at which the
    # JWT was issued.
    payload["iat"] = datetime.utcnow()

    # The "sub" (subject) claim identifies the principal that is the
    # subject of the JWT
    payload["sub"] = str(sub)
    return jwt.encode(
        payload, settings.auth.JWT_SECRET, algorithm=settings.auth.ALGORITHM
    )
