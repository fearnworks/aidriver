# Import all the models, so that Base has them before being
# imported by Alembic
from ai_driver.server.db.base_class import Base  # noqa
from ai_driver.server.models.user import User  # noqa
