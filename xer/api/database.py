import sqlite3
from pathlib import Path
from typing import Generator

# Define the path relative to the project root
# xer/api/database.py -> xer/api -> xer -> root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data" / "contos.sqlite"

def get_db() -> Generator[sqlite3.Connection, None, None]:
    """
    Creates a database connection to the SQLite database.
    Yields the connection so it can be used as a dependency.
    Closes the connection after use.
    """
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
