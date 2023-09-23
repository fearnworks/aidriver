"""
This module provides CRUD operations for User objects in the database. It includes functions for
creating, reading, and updating User objects. It extends the base CRUDBase class.
"""

from typing import Any, Dict, Optional, Union

from ai_driver.server.core.security import get_password_hash
from ai_driver.server.crud.base import CRUDBase
from ai_driver.server.models.user import User
from ai_driver.server.schemas.user import UserCreate, UserUpdate
from sqlalchemy.orm import Session


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """
    Class for User CRUD operations, inheriting from CRUDBase.
    """

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        Get a User object by email.

        Args:
            db (Session): The database session.
            email (str): The email of the user.

        Returns:
            Optional[User]: The User object, if found. Else, None.
        """
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        Create a new User object.

        Args:
            db (Session): The database session.
            obj_in (UserCreate): A UserCreate object containing user details.

        Returns:
            User: The created User object.
        """
        create_data = obj_in.dict()
        create_data.pop("password")
        db_obj = User(**create_data)
        db_obj.hashed_password = get_password_hash(obj_in.password)
        db.add(db_obj)
        db.commit()

        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """
        Update a User object.

        Args:
            db (Session): The database session.
            db_obj (User): The User object to update.
            obj_in (Union[UserUpdate, Dict[str, Any]]): New data for update.

        Returns:
            User: The updated User object.
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def is_superuser(self, user: User) -> bool:
        """
        Check if a User is a superuser.

        Args:
            user (User): The User object to check.

        Returns:
            bool: True if the user is a superuser, False otherwise.
        """
        return user.is_superuser


# Create a CRUDUser object for User model to perform CRUD operations.
user = CRUDUser(User)
