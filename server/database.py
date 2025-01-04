import os
from google.cloud.sql.connector import Connector
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

# Initialize the Cloud SQL Connector
connector = Connector()

# Declarative Base for ORM
Base = declarative_base()

def get_sqlalchemy_engine():
    """
    Create an SQLAlchemy engine with Google Cloud SQL Connector.
    """
    def get_connection():
        return connector.connect(
            os.getenv("CLOUD_SQL_CONNECTION_NAME"),
            "pymysql",
            user=os.getenv("CLOUDSQL_USER"),
            password=os.getenv("CLOUDSQL_PASSWORD"),
            db=os.getenv("CLOUDSQL_DB"),
        )

    engine = create_engine(
        "mysql+pymysql://",
        creator=get_connection,
        pool_size=5,  # Adjust based on your application
        max_overflow=2,
        pool_timeout=30,  # Timeout in seconds for connections
    )
    return engine


# Create SQLAlchemy Engine and SessionLocal
engine = get_sqlalchemy_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """
    Initialize the database schema using SQLAlchemy ORM.
    """
    with engine.connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
    Base.metadata.create_all(bind=engine)
