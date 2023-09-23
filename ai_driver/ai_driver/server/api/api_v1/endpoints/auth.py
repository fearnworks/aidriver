"""
This module defines API endpoints related to user authentication such as login, fetching logged in user's info,
and user signup in a FastAPI application.

TODO - Consider enhanced error handling and validation
"""
from loguru import logger
from typing import Any

import ai_driver.server.api.deps as deps
import ai_driver.server.crud as crud
import ai_driver.server.schemas as schemas
from ai_driver.server.core.auth import authenticate, create_access_token
from ai_driver.server.models.user import User
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

router = APIRouter()


@router.post("/login")
def login(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Authenticate a user and return a JWT.

    The function takes a SQLAlchemy Session and OAuth2PasswordRequestForm data as dependencies.
    If the user's credentials are valid, a JWT is returned.

    Args:
        db (Session): SQLAlchemy Session.
        form_data (OAuth2PasswordRequestForm): Form data containing user's credentials.

    Returns:
        dict: A dictionary containing the access token and token type.
    """
    logger.info(form_data)
    user = authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": create_access_token(sub=user.id),
        "token_type": "bearer",
    }


@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: User = Depends(deps.get_current_user)):
    """
    Get the current logged in user.

    Args:
        current_user (User): Current logged in user.

    Returns:
        User: The current logged in user.
    """

    return current_user


@router.post("/signup", response_model=schemas.User, status_code=201)
def create_user_signup(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserCreate,
) -> Any:
    """
    Create a new user.

    This function creates a new user with the provided user information.
    If a user with the same email already exists, an error is raised.

    Args:
        db (Session): SQLAlchemy Session.
        user_in (schemas.user.UserCreate): User input data.

    Returns:
        User: The created user.
    """

    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = crud.user.create(db=db, obj_in=user_in)

    return user
