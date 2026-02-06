from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
import sqlite3
from xer.api.database import get_db
from xer.api.models import TaleSummary, TaleDetail, TaleListResponse

router = APIRouter(prefix="/tales", tags=["Tales"])


def get_classifications_for_tales(conn: sqlite3.Connection, tale_ids: List[int]):
    # Note: classifications tables are missing in the new schema.
    # Returning empty classifications for now.
    return {tale_id: [] for tale_id in tale_ids}


@router.get("", response_model=TaleListResponse)
async def list_tales(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    conn: sqlite3.Connection = Depends(get_db),
):
    offset = (page - 1) * page_size

    # Get total count
    total = conn.execute("SELECT COUNT(*) FROM tales").fetchone()[0]

    # Get tales joining with translations
    cursor = conn.execute(
        """
        SELECT t.id, tr.title as titulo, t.source as origem, t.url, t.author, t.region
        FROM tales t
        JOIN tale_translations tr ON t.id = tr.tale_id
        WHERE tr.language_code = 'en'
        LIMIT ? OFFSET ?
        """,
        (page_size, offset),
    )
    tales_rows = cursor.fetchall()

    tale_ids = [row["id"] for row in tales_rows]
    classifications_map = get_classifications_for_tales(conn, tale_ids)

    tales = []
    for row in tales_rows:
        author = row["author"]
        region = row["region"]

        metadata_parts = []
        if author:
            metadata_parts.append(author)
        if region:
            if author:
                metadata_parts.append(f"({region})")
            else:
                metadata_parts.append(region)

        metadata = " ".join(metadata_parts) if metadata_parts else None

        tales.append(
            TaleSummary(
                id=row["id"],
                titulo=row["titulo"],
                author=author,
                region=region,
                source=row["origem"],
                metadata=metadata,
                url=row["url"],
                classifications=classifications_map.get(row["id"], []),
            )
        )

    return TaleListResponse(tales=tales, total=total, page=page, page_size=page_size)


@router.get("/search", response_model=TaleListResponse)
async def search_tales(
    title: Optional[str] = None,
    text: Optional[str] = None,
    framework: Optional[str] = None,
    classification: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    conn: sqlite3.Connection = Depends(get_db),
):
    offset = (page - 1) * page_size

    query_parts = [
        """
        SELECT DISTINCT t.id, tr.title as titulo, t.source as origem, t.url, t.author, t.region
        FROM tales t
        JOIN tale_translations tr ON t.id = tr.tale_id
        """
    ]
    count_query_parts = [
        """
        SELECT COUNT(DISTINCT t.id) 
        FROM tales t
        JOIN tale_translations tr ON t.id = tr.tale_id
        """
    ]
    where_clauses = ["tr.language_code = 'en'"]
    params = []

    # Skip joins for classifications as tables don't exist
    if title:
        where_clauses.append("tr.title LIKE ?")
        params.append(f"%{title}%")

    if text:
        where_clauses.append("tr.story_body LIKE ?")
        params.append(f"%{text}%")

    # Note: framework/classification filtering is disabled

    full_query = query_parts[0]
    full_count_query = count_query_parts[0]

    if where_clauses:
        full_query += " WHERE " + " AND ".join(where_clauses)
        full_count_query += " WHERE " + " AND ".join(where_clauses)

    # Execute count
    total = conn.execute(full_count_query, params).fetchone()[0]

    # Execute search
    full_query += " LIMIT ? OFFSET ?"
    search_params = params + [page_size, offset]

    cursor = conn.execute(full_query, search_params)
    tales_rows = cursor.fetchall()

    tale_ids = [row["id"] for row in tales_rows]
    classifications_map = get_classifications_for_tales(conn, tale_ids)

    tales = []
    for row in tales_rows:
        author = row["author"]
        region = row["region"]

        metadata_parts = []
        if author:
            metadata_parts.append(author)
        if region:
            if author:
                metadata_parts.append(f"({region})")
            else:
                metadata_parts.append(region)

        metadata = " ".join(metadata_parts) if metadata_parts else None

        tales.append(
            TaleSummary(
                id=row["id"],
                titulo=row["titulo"],
                author=author,
                region=region,
                source=row["origem"],
                metadata=metadata,
                url=row["url"],
                classifications=classifications_map.get(row["id"], []),
            )
        )

    return TaleListResponse(tales=tales, total=total, page=page, page_size=page_size)


@router.get("/classification/{framework}/{name}", response_model=TaleListResponse)
async def get_tales_by_classification(
    framework: str,
    name: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    conn: sqlite3.Connection = Depends(get_db),
):
    return await search_tales(
        framework=framework,
        classification=name,
        page=page,
        page_size=page_size,
        conn=conn,
    )


@router.get("/keywords", response_model=TaleListResponse)
async def search_keywords(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    conn: sqlite3.Connection = Depends(get_db),
):
    # The FTS table might have changed or be missing columns required by the API.
    # We'll proxy to search_tales to ensure compatibility with the current schema.
    return await search_tales(text=q, page=page, page_size=page_size, conn=conn)


@router.get("/{id}", response_model=TaleDetail)
async def get_tale(id: int, conn: sqlite3.Connection = Depends(get_db)):
    row = conn.execute(
        """
        SELECT t.id, tr.title as titulo, t.source as origem, t.url, tr.story_body as texto_completo, t.author, t.region 
        FROM tales t
        JOIN tale_translations tr ON t.id = tr.tale_id
        WHERE t.id = ? AND tr.language_code = 'en'
        """,
        (id,),
    ).fetchone()

    if not row:
        raise HTTPException(status_code=404, detail="Tale not found")

    classifications_map = get_classifications_for_tales(conn, [id])

    author = row["author"]
    region = row["region"]

    metadata_parts = []
    if author:
        metadata_parts.append(author)
    if region:
        if author:
            metadata_parts.append(f"({region})")
        else:
            metadata_parts.append(region)

    metadata = " ".join(metadata_parts) if metadata_parts else None

    return TaleDetail(
        id=row["id"],
        titulo=row["titulo"],
        author=author,
        region=region,
        source=row["origem"],
        metadata=metadata,
        url=row["url"],
        texto_completo=row["texto_completo"],
        classifications=classifications_map.get(id, []),
    )
