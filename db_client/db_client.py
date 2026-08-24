import psycopg2

from resources.db_creds import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
)


def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )


def check_db_connection():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT version();")

    version = cur.fetchone()
    print(f"PostgreSQL version: {version[0]}")

    cur.close()
    conn.close()