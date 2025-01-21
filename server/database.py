import os

import sqlalchemy

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()


def init_connection_pool():
    # Fetch environment variables or default values for the database connection
    db_user = os.getenv("DB_USER", "user")  # Replace 'user' with your default user
    db_password = os.getenv("DB_PASSWORD", "password")  # Replace 'password' with your default password
    db_host = os.getenv("DB_HOST", "localhost")  # Replace 'localhost' with your default host
    db_port = os.getenv("DB_PORT", "5432")  # Replace '5432' with your default port
    db_name = os.getenv("DB_NAME", "database")  # Replace 'database' with your default database name

    # Create the PostgreSQL connection string
    connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    # Create an SQLAlchemy engine with a connection pool
    engine = create_engine(
        connection_string,
        pool_size=5,  # Adjust pool size as needed
        max_overflow=10,  # Allows additional connections if the pool is full
        pool_timeout=30,  # Wait time before raising a timeout error
        echo=True  # Enable SQLAlchemy query logging for debugging
    )

    # Test the connection
    try:
        with engine.connect() as connection:
            print("Successfully connected to the database.")
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

    return engine


# create 'votes' table in database if it does not already exist
def migrate_db(db: sqlalchemy.engine.base.Engine) -> None:
    """Creates the `votes` table if it doesn't exist."""
    # Base.metadata.create_all(bind=db)

    with db.connect() as conn:
        conn.execute(
            sqlalchemy.text(
                "CREATE TABLE IF NOT EXISTS documents "
                "(  id SERIAL PRIMARY KEY, "
                "title VARCHAR(255) NOT NULL, "
                "content TEXT NOT NULL, "
                "created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP );"
            )
        )
        conn.commit()


# This global variable is declared with a value of `None`, instead of calling
# `init_db()` immediately, to simplify testing. In general, it
# is safe to initialize your database connection pool when your script starts
# -- there is no need to wait for the first request.
db = None