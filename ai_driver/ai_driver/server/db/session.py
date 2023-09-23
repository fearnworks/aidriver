"""
This module defines the `engine` and `SessionLocal` objects used to interact
with the database.

The `engine` object is an instance of `sqlalchemy.create_engine` and is used to
connect to the database.

The `SessionLocal` object is an instance of `sqlalchemy.orm.sessionmaker` and is
used to create new sessions for interacting with the database.
"""

from ai_driver.server.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Heroku workaround: https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
connection_uri = settings.db.SQLALCHEMY_DATABASE_URI

# Detect the type of the database
if connection_uri.startswith("sqlite://"):
    print("The database is SQLite.")
elif connection_uri.startswith("postgresql://"):
    print("The database is PostgreSQL.")
elif connection_uri.startswith("mysql://"):
    print("The database is MySQL.")
elif connection_uri.startswith("oracle://"):
    print("The database is Oracle.")
elif connection_uri.startswith("mssql://"):
    print("The database is SQL Server.")
elif connection_uri.startswith("mssql+pymssql://"):
    print("The database is SQL Server with the pymssql driver.")
else:
    print("Unknown database type.")

if connection_uri.startswith("postgres://"):
    connection_uri = connection_uri.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    connection_uri,
)

# Create a session factory with thread awareness
SessionLocal = sessionmaker(bind=engine)
