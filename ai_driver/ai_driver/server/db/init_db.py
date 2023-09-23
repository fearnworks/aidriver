from loguru import logger

import ai_driver.server.schemas.user as UserSchema
from ai_driver.server.core.config import settings
from ai_driver.server.crud.crud_user import user as crudUser
from ai_driver.server.db import base  # noqa: F401
from sqlalchemy.orm import Session


# make sure all SQL Alchemy models are imported (ai_driver.server.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)
    if settings.db.FIRST_SUPERUSER:
        user = crudUser.get_by_email(db, email=settings.db.FIRST_SUPERUSER)
        if not user:
            user_in = UserSchema.UserCreate(
                first_name="admin",
                surname="mcgee",
                email=settings.db.FIRST_SUPERUSER,
                is_superuser=True,
                password=settings.db.FIRST_SUPERUSER_PW,
            )
            user = crudUser.create(db, obj_in=user_in)  # noqa: F841
        else:
            logger.warning(
                "Skipping creating superuser. User with email "
                f"{settings.db.FIRST_SUPERUSER} already exists. "
            )

    else:
        logger.warning(
            "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
            "provided as an env variable. "
            "e.g.  FIRST_SUPERUSER=admin@api.datawarehouse.com"
        )
