from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from resources.db_creds import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD
)


connection_string = (
    f"postgresql+psycopg2://"
    f"{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(connection_string, echo=False)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db_session():
    return SessionLocal()


def check_db_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        print(f"PostgreSQL version: {result.fetchone()[0]}")