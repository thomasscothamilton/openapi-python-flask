import os
from google.cloud.sql.connector import Connector
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Cloud SQL Connector
connector = Connector()

# Declarative Base for ORM
Base = declarative_base()

# SQLAlchemy Engine and Session
def get_sqlalchemy_engine():
    """
    Create an SQLAlchemy engine using DATABASE_URL if available.
    Falls back to Google Cloud SQL Connector if DATABASE_URL is not set.
    """
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # Use DATABASE_URL for local development or other configurations
        return create_engine(database_url, echo=True)

    # Use Google Cloud SQL Connector if DATABASE_URL is not provided
    connection_name = os.getenv("CLOUD_SQL_CONNECTION_NAME")
    if not connection_name:
        raise ValueError("CLOUD_SQL_CONNECTION_NAME is not set and DATABASE_URL is missing.")

    def get_connection():
        return connector.connect(
            connection_name,
            "pymysql",
            user=os.getenv("CLOUDSQL_USER"),
            password=os.getenv("CLOUDSQL_PASSWORD"),
            db=os.getenv("CLOUDSQL_DB"),
        )

    return create_engine(
        "mysql+pymysql://",
        creator=get_connection,
        pool_size=5,
        max_overflow=2,
        pool_timeout=30,
    )


# Initialize SQLAlchemy Engine and Session
engine = get_sqlalchemy_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Initialize the database schema using SQLAlchemy ORM.
    """
    from server.models.document import Document  # Import all models here to ensure they are registered
    Base.metadata.create_all(bind=engine)
