"""
This module provides a generic class for CRUD (Create, Read, Update, Delete) operations. This class
can be used as a base class for concrete implementations of CRUD operations for different models.

TODO:
1. Add type checking for the `id` parameter in the `get` and `remove` methods. Currently, `id` is typed as `Any`,
   but it might be more appropriate to restrict it to integer or string types, which are commonly used as identifiers.
2. Add error handling in the `remove` method. If there is no object with the given id, the `delete` operation may fail.
   We could handle this by raising a custom exception if `obj` is `None`.
3. Extend this class to support more complex query operations, like filtering and sorting, if needed.
"""
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from ai_driver.server.db.base_class import Base
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Generic CRUD base class with default methods to Create, Read, Update, and Delete (CRUD).
    """

    def __init__(self, model: Type[ModelType]):
        """
        Initialize CRUDBase with the model type.

        Args:
            model (Type[ModelType]): A SQLAlchemy model class reference.
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        Get a single record by id.

        Args:
            db (Session): Database session.
            id (Any): Id of the record.

        Returns:
            Optional[ModelType]: An instance of the model or None.
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 5000
    ) -> List[ModelType]:
        """
        Get multiple records with pagination.

        Args:
            db (Session): Database session.
            skip (int, optional): Number of records to skip. Defaults to 0.
            limit (int, optional): Maximum number of records to return. Defaults to 5000.

        Returns:
            List[ModelType]: A list of model instances.
        """
        return (
            db.query(self.model).order_by(self.model.id).offset(skip).limit(limit).all()
        )

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record.

        Args:
            db (Session): Database session.
            obj_in (CreateSchemaType): Pydantic schema with fields to create a new record.

        Returns:
            ModelType: The created model instance.
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update an existing record.

        Args:
            db (Session): Database session.
            db_obj (ModelType): The existing model instance to update.
            obj_in (Union[UpdateSchemaType, Dict[str, Any]]): Pydantic schema or dict with fields to update.

        Returns:
            ModelType: The updated model instance.
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """
        Remove a record.

        Args:
            db (Session): Database session.
            id (int): Id of the record to remove.

        Returns:
            ModelType: The removed model instance.
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
