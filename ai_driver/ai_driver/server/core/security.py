"""
This module provides functionality to handle password encryption and verification using bcrypt.
"""

from passlib.context import CryptContext

# Create a password context for bcrypt
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hashed password.

    Args:
        plain_password (str): The plain text password.
        hashed_password (str): The hashed password for comparison.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password (str): The plain text password.

    Returns:
        str: The hashed password.
    """
    return PWD_CONTEXT.hash(password)
