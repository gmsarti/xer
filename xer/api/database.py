import sqlite3
from typing import Generator
from xer.config import get_settings

settings = get_settings()


def get_db() -> Generator[sqlite3.Connection, None, None]:
    """
    Creates a database connection to the SQLite database.
    Yields the connection so it can be used as a dependency.
    Closes the connection after use.
    """
    db_url = settings.database_url
    # Extract path from database_url (format: sqlite:///./data/xer.db)
    db_path = db_url.replace("sqlite:///", "")

    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
