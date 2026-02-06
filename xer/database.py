"""Database module for SQLite operations."""

import sqlite3
import random
from datetime import date
from pathlib import Path
from typing import Any, Optional

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
                SELECT t.id, tr.title as title, tr.story_body as text, t.source as source, t.author as author, t.region as region, t.selection_count
                FROM tales t
                JOIN tale_translations tr ON t.id = tr.tale_id
                WHERE tr.language_code = 'en'
                ORDER BY t.id DESC
                LIMIT ? OFFSET ?
                """,
                (limit, offset),
            )

            tales = []
            for row in cursor.fetchall():
                tale_dict = dict(row)
                author = tale_dict.get("author")
                region = tale_dict.get("region")

                metadata_parts = []
                if author:
                    metadata_parts.append(author)
                if region:
                    if author:
                        metadata_parts.append(f"({region})")
                    else:
                        metadata_parts.append(region)

                tale_dict["metadata"] = (
                    " ".join(metadata_parts) if metadata_parts else None
                )
                tales.append(tale_dict)

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
                SELECT t.id, tr.title as title, tr.story_body as text, t.source as source, t.author as author, t.region as region, t.selection_count
                FROM tales t
                JOIN tale_translations tr ON t.id = tr.tale_id
                WHERE t.id = ? AND tr.language_code = 'en'
                """,
                (tale_id,),
            )

            row = cursor.fetchone()
            if row:
                tale_dict = dict(row)
                author = tale_dict.get("author")
                region = tale_dict.get("region")

                metadata_parts = []
                if author:
                    metadata_parts.append(author)
                if region:
                    if author:
                        metadata_parts.append(f"({region})")
                    else:
                        metadata_parts.append(region)

                tale_dict["metadata"] = (
                    " ".join(metadata_parts) if metadata_parts else None
                )
                return tale_dict
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
                    SELECT t.id, tr.title as title, tr.story_body as text, t.source as source, t.author as author, t.region as region, t.selection_count
                    FROM tales t
                    JOIN tale_translations tr ON t.id = tr.tale_id
                    WHERE tr.language_code = 'en'
                    ORDER BY t.id DESC
                    LIMIT ?
                    """,
                    (limit,),
                )
            else:
                # Search in title and text
                search_pattern = f"%{query}%"
                cursor.execute(
                    """
                    SELECT t.id, tr.title as title, tr.story_body as text, t.source as source, t.author as author, t.region as region, t.selection_count
                    FROM tales t
                    JOIN tale_translations tr ON t.id = tr.tale_id
                    WHERE tr.language_code = 'en' AND (tr.title LIKE ? OR tr.story_body LIKE ?)
                    ORDER BY
                        CASE
                            WHEN tr.title LIKE ? THEN 1
                            ELSE 2
                        END,
                        t.id DESC
                    LIMIT ?
                    """,
                    (search_pattern, search_pattern, search_pattern, limit),
                )

            tales = []
            for row in cursor.fetchall():
                tale_dict = dict(row)
                author = tale_dict.get("author")
                region = tale_dict.get("region")

                metadata_parts = []
                if author:
                    metadata_parts.append(author)
                if region:
                    if author:
                        metadata_parts.append(f"({region})")
                    else:
                        metadata_parts.append(region)

                tale_dict["metadata"] = (
                    " ".join(metadata_parts) if metadata_parts else None
                )
                tales.append(tale_dict)

            logger.debug(
                f"Found {len(tales)} tales for query '{query}' (limit={limit})"
            )
            return tales

    except sqlite3.Error as e:
        logger.error(f"Database error while searching tales: {e}")
        return []


def get_random_tale(
    seed: Optional[str] = None, increment: bool = True
) -> dict[str, Any] | None:
    """Get a random tale among those with the minimum selection_count.

    Args:
        seed: Optional seed for reproducible randomization.
        increment: Whether to increment the selection count.

    Returns:
       Tale dictionary or None if error/no tales
    """
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Find minimum selection count
            cursor.execute("SELECT MIN(selection_count) FROM tales")
            min_count_row = cursor.fetchone()
            if min_count_row is None or min_count_row[0] is None:
                min_count = 0
            else:
                min_count = min_count_row[0]

            # Get all candidate IDs
            cursor.execute(
                "SELECT id FROM tales WHERE selection_count = ?", (min_count,)
            )
            candidate_ids = [row["id"] for row in cursor.fetchall()]

            if not candidate_ids:
                return None

            # Seed and pick
            if seed:
                random.seed(seed)
            tale_id = random.choice(candidate_ids)

            if increment:
                # Increment count
                cursor.execute(
                    "UPDATE tales SET selection_count = selection_count + 1 WHERE id = ?",
                    (tale_id,),
                )
                conn.commit()

            # Return the full tale data
            return get_tale(tale_id)

    except sqlite3.Error as e:
        logger.error(f"Database error while fetching random tale: {e}")
        return None


def get_or_create_daily_tale() -> dict[str, Any] | None:
    """Get the tale for today, creating it if it doesn't exist.

    Returns:
        The tale of the day or None
    """
    today = date.today().isoformat()
    try:
        with get_connection() as conn:
            cursor = conn.cursor()

            # Check if we already have a tale for today
            cursor.execute("SELECT tale_id FROM daily_tales WHERE day = ?", (today,))
            row = cursor.fetchone()
            if row:
                return get_tale(row["tale_id"])

            # If not, get a new one (with increment)
            # We use the date as seed to ensure consistency if multiple workers try to create it
            # simultaneously (though incrementing might still happen twice if not careful,
            # but ISO date seed helps keep it stable).
            # Actually, the requirement says "salvar no banco toda vez que uma história foi selecionada randomicamente".
            # For the daily tale, it's selected once per day.

            tale = get_random_tale(increment=True)
            if not tale:
                return None

            # Save to daily_tales
            try:
                cursor.execute(
                    "INSERT INTO daily_tales (day, tale_id) VALUES (?, ?)",
                    (today, tale["id"]),
                )
                conn.commit()
            except sqlite3.IntegrityError:
                # Another process might have inserted it just now
                conn.rollback()
                cursor.execute(
                    "SELECT tale_id FROM daily_tales WHERE day = ?", (today,)
                )
                row = cursor.fetchone()
                if row:
                    return get_tale(row["tale_id"])

            return tale

    except sqlite3.Error as e:
        logger.error(f"Database error while handling daily tale: {e}")
        return None
