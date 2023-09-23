"""
This module defines the Pydantic models for the User entity. These models are used for data validation,
serialization and deserialization.

TODO:
1. Define what the UserUpdate model should contain. The current `...` placeholder indicates it's not complete.
2. Explicitly define the fields in the User model instead of using `...`.
3. Validate email format in UserBase.
4. Consider adding more comments to explain what each model represents, especially the difference
   between `User`, `UserInDB` and `UserInDBBase`.
"""

from typing import Optional

from pydantic import BaseModel, EmailStr, Field
import uuid


class UserBase(BaseModel):
    """
    A base model for user that includes the common attributes.
    """

    first_name: str | None
    surname: str | None
    email: Optional[EmailStr] = None
    is_superuser: bool = False
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))


class UserCreate(UserBase):
    """
    A model for user creation. It includes all the attributes required to create a user.
    """

    email: EmailStr
    password: str


class UserUpdate(UserBase):
    """
    A model for user update operations. It includes all the attributes that can be updated.
    """

    ...


class UserInDBBase(UserBase):
    """
    A base model for users stored in the database. It includes the id attribute.
    """

    id: str

    class Config:
        from_attributes = True


class UserInDB(UserInDBBase):
    """
    A model for users stored in the database. It includes the hashed_password attribute.
    """

    hashed_password: str


class User(UserInDBBase):
    """
    A model for users to be returned to the client. It inherits from UserInDBBase.
    """

    ...
