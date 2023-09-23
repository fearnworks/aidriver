"""
This module defines the `User` model, which represents a user in the
application.

The `User` model has several attributes, including `id`, `first_name`,
`surname`, `email`, `is_superuser`, and `hashed_password`.
"""

from ai_driver.server.db.base_class import Base
from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship


class User(Base):
    """
    Represents a user in the application.

    Attributes:
        id: The primary key of the model.
        first_name: The first name of the user.
        surname: The surname of the user.
        email: The email address of the user.
        is_superuser: Whether or not the user is a superuser.
        hashed_password: The hashed password of the user.
    """

    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=True)
    surname = Column(String(256), nullable=True)
    email = Column(String, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)

    # New addition
    hashed_password = Column(String, nullable=False)
