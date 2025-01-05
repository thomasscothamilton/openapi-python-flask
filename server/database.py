import os

import sqlalchemy

from server.connect_connector_auto_iam_authn import connect_with_connector_auto_iam_authn
from server.connect_tcp import connect_tcp_socket
from server.connect_unix import connect_unix_socket

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from server.connect_connector import connect_with_connector

Base = declarative_base()

def init_connection_pool() -> sqlalchemy.engine.base.Engine:
    """Sets up connection pool for the app."""
    if os.environ.get("USE_SQLITE"):
        # Use SQLite for local development or testing
        sqlite_path = os.path.join(os.path.dirname(__file__), "local.db")
        return sqlalchemy.create_engine(f"sqlite:///{sqlite_path}", connect_args={"check_same_thread": False})

    # use a TCP socket when INSTANCE_HOST (e.g. 127.0.0.1) is defined
    if os.environ.get("INSTANCE_HOST"):
        return connect_tcp_socket()

    # use a Unix socket when INSTANCE_UNIX_SOCKET (e.g. /cloudsql/project:region:instance) is defined
    if os.environ.get("INSTANCE_UNIX_SOCKET"):
        return connect_unix_socket()

    # use the connector when INSTANCE_CONNECTION_NAME (e.g. project:region:instance) is defined
    if os.environ.get("INSTANCE_CONNECTION_NAME"):
        # Either a DB_USER or a DB_IAM_USER should be defined. If both are
        # defined, DB_IAM_USER takes precedence.
        return (
            connect_with_connector_auto_iam_authn()
            if os.environ.get("DB_IAM_USER")
            else connect_with_connector()
        )

    raise ValueError(
        "Missing database connection type. Please define one of INSTANCE_HOST, INSTANCE_UNIX_SOCKET, or INSTANCE_CONNECTION_NAME"
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=init_connection_pool())

# create 'votes' table in database if it does not already exist
def migrate_db(db: sqlalchemy.engine.base.Engine) -> None:
    """Creates the `votes` table if it doesn't exist."""
    # Base.metadata.create_all(bind=db)

    with db.connect() as conn:
        conn.execute(
            sqlalchemy.text(
                "CREATE TABLE IF NOT EXISTS documents "
                "( id INTEGER PRIMARY KEY AUTOINCREMENT, "
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