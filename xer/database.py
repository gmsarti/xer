"""Database module for SQLite operations."""

import sqlite3
from pathlib import Path
from typing import Any

from xer.config import get_settings
from xer.logger import logger

settings = get_settings()


def get_connection() -> sqlite3.Connection:
    """Get a connection to the SQLite database.

    Returns:
        sqlite3.Connection: Database connection
    """
    # Extract path from database_url (format: sqlite:///./data/xer.db)
    db_path = settings.database_url.replace("sqlite:///", "")

    logger.info(f"Connecting to database: {db_path}")

    # Ensure the data directory exists
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Allow dict-like access to rows
    return conn


def list_tales(limit: int = 20, offset: int = 0) -> list[dict[str, Any]]:
    """List tales with pagination.

    Args:
        limit: Maximum number of tales to return
        offset: Number of tales to skip

    Returns:
        List of tale dictionaries
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT id, titulo as title, texto_completo as text, origem as source
            FROM tales
            ORDER BY id DESC
            LIMIT ? OFFSET ?
            """,
            (limit, offset),
        )

        tales = [dict(row) for row in cursor.fetchall()]
        logger.debug(f"Retrieved {len(tales)} tales (limit={limit}, offset={offset})")
        return tales

    except sqlite3.Error as e:
        logger.error(f"Database error while listing tales: {e}")
        return []
    finally:
        conn.close()


def get_tale(tale_id: int) -> dict[str, Any] | None:
    """Get a single tale by ID.

    Args:
        tale_id: The ID of the tale to retrieve

    Returns:
        Tale dictionary or None if not found
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            SELECT id, titulo as title, texto_completo as text, origem as source
            FROM tales
            WHERE id = ?
            """,
            (tale_id,),
        )

        row = cursor.fetchone()
        if row:
            return dict(row)
        return None

    except sqlite3.Error as e:
        logger.error(f"Database error while fetching tale {tale_id}: {e}")
        return None
    finally:
        conn.close()
