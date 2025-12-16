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
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
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
            logger.debug(
                f"Retrieved {len(tales)} tales (limit={limit}, offset={offset})"
            )
            return tales

    except sqlite3.Error as e:
        logger.error(f"Database error while listing tales: {e}")
        return []


def get_tale(tale_id: int) -> dict[str, Any] | None:
    """Get a single tale by ID.

    Args:
        tale_id: The ID of the tale to retrieve

    Returns:
        Tale dictionary or None if not found
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
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


def search_tales(query: str = "", limit: int = 50) -> list[dict[str, Any]]:
    """Search tales by text query.

    Args:
        query: Search query (searches in title and text)
        limit: Maximum number of results to return

    Returns:
        List of tale dictionaries matching the query
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            if not query or query.strip() == "":
                # If no query, return recent tales
                cursor.execute(
                    """
                    SELECT id, titulo as title, texto_completo as text, origem as source
                    FROM tales
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (limit,),
                )
            else:
                # Search in title and text
                search_pattern = f"%{query}%"
                cursor.execute(
                    """
                    SELECT id, titulo as title, texto_completo as text, origem as source
                    FROM tales
                    WHERE titulo LIKE ? OR texto_completo LIKE ?
                    ORDER BY
                        CASE
                            WHEN titulo LIKE ? THEN 1
                            ELSE 2
                        END,
                        id DESC
                    LIMIT ?
                    """,
                    (search_pattern, search_pattern, search_pattern, limit),
                )

            tales = [dict(row) for row in cursor.fetchall()]
            logger.debug(
                f"Found {len(tales)} tales for query '{query}' (limit={limit})"
            )
            return tales

    except sqlite3.Error as e:
        logger.error(f"Database error while searching tales: {e}")
        return []
