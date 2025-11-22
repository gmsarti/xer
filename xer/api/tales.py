from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
import sqlite3
from xer.api.database import get_db
from xer.api.models import TaleSummary, TaleDetail, TaleListResponse, Classification

router = APIRouter(prefix="/tales", tags=["Tales"])

def get_classifications_for_tales(conn: sqlite3.Connection, tale_ids: List[int]):
    if not tale_ids:
        return {}
    
    placeholders = ",".join("?" * len(tale_ids))
    query = f"""
        SELECT cc.conto_id, c.framework, c.nome_classificacao as name
        FROM conto_classificacao cc
        JOIN classificacoes c ON cc.classificacao_id = c.classificacao_id
        WHERE cc.conto_id IN ({placeholders})
    """
    cursor = conn.execute(query, tale_ids)
    rows = cursor.fetchall()
    
    classifications_map = {tale_id: [] for tale_id in tale_ids}
    for row in rows:
        classifications_map[row["conto_id"]].append(
            Classification(framework=row["framework"], name=row["name"])
        )
    return classifications_map

@router.get("", response_model=TaleListResponse)
async def list_tales(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    conn: sqlite3.Connection = Depends(get_db)
):
    offset = (page - 1) * page_size
    
    # Get total count
    total = conn.execute("SELECT COUNT(*) FROM tales").fetchone()[0]
    
    # Get tales
    cursor = conn.execute(
        "SELECT id, titulo, origem, url FROM tales LIMIT ? OFFSET ?",
        (page_size, offset)
    )
    tales_rows = cursor.fetchall()
    
    tale_ids = [row["id"] for row in tales_rows]
    classifications_map = get_classifications_for_tales(conn, tale_ids)
    
    tales = []
    for row in tales_rows:
        tales.append(
            TaleSummary(
                id=row["id"],
                titulo=row["titulo"],
                origem=row["origem"],
                url=row["url"],
                classifications=classifications_map.get(row["id"], [])
            )
        )
        
    return TaleListResponse(
        tales=tales,
        total=total,
        page=page,
        page_size=page_size
    )

@router.get("/search", response_model=TaleListResponse)
async def search_tales(
    title: Optional[str] = None,
    text: Optional[str] = None,
    framework: Optional[str] = None,
    classification: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    conn: sqlite3.Connection = Depends(get_db)
):
    offset = (page - 1) * page_size
    
    query_parts = ["SELECT DISTINCT t.id, t.titulo, t.origem, t.url FROM tales t"]
    count_query_parts = ["SELECT COUNT(DISTINCT t.id) FROM tales t"]
    where_clauses = []
    params = []
    
    joins = []
    
    if framework or classification:
        joins.append("JOIN conto_classificacao cc ON t.id = cc.conto_id")
        joins.append("JOIN classificacoes c ON cc.classificacao_id = c.classificacao_id")
        
    if title:
        where_clauses.append("t.titulo LIKE ?")
        params.append(f"%{title}%")
        
    if text:
        where_clauses.append("t.texto_completo LIKE ?")
        params.append(f"%{text}%")
        
    if framework:
        where_clauses.append("c.framework = ?")
        params.append(framework)
        
    if classification:
        where_clauses.append("c.nome_classificacao = ?")
        params.append(classification)
        
    full_query = query_parts[0]
    full_count_query = count_query_parts[0]
    
    if joins:
        full_query += " " + " ".join(joins)
        full_count_query += " " + " ".join(joins)
        
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
        tales.append(
            TaleSummary(
                id=row["id"],
                titulo=row["titulo"],
                origem=row["origem"],
                url=row["url"],
                classifications=classifications_map.get(row["id"], [])
            )
        )
        
    return TaleListResponse(
        tales=tales,
        total=total,
        page=page,
        page_size=page_size
    )

@router.get("/classification/{framework}/{name}", response_model=TaleListResponse)
async def get_tales_by_classification(
    framework: str,
    name: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    conn: sqlite3.Connection = Depends(get_db)
):
    return await search_tales(
        framework=framework,
        classification=name,
        page=page,
        page_size=page_size,
        conn=conn
    )

@router.get("/keywords", response_model=TaleListResponse)
async def search_keywords(
    q: str = Query(..., min_length=1),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    conn: sqlite3.Connection = Depends(get_db)
):
    # Try to use FTS5 if available, otherwise fallback to LIKE
    offset = (page - 1) * page_size
    
    # Check if FTS table exists
    fts_exists = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='tales_fts'"
    ).fetchone()
    
    if fts_exists:
        # Use FTS
        count_query = "SELECT COUNT(*) FROM tales_fts WHERE tales_fts MATCH ?"
        total = conn.execute(count_query, (q,)).fetchone()[0]
        
        query = """
            SELECT t.id, t.titulo, t.origem, t.url
            FROM tales t
            JOIN tales_fts fts ON t.id = fts.rowid
            WHERE fts.tales_fts MATCH ?
            ORDER BY fts.rank
            LIMIT ? OFFSET ?
        """
        cursor = conn.execute(query, (q, page_size, offset))
    else:
        # Fallback to LIKE
        return await search_tales(text=q, page=page, page_size=page_size, conn=conn)

    tales_rows = cursor.fetchall()
    tale_ids = [row["id"] for row in tales_rows]
    classifications_map = get_classifications_for_tales(conn, tale_ids)
    
    tales = []
    for row in tales_rows:
        tales.append(
            TaleSummary(
                id=row["id"],
                titulo=row["titulo"],
                origem=row["origem"],
                url=row["url"],
                classifications=classifications_map.get(row["id"], [])
            )
        )
        
    return TaleListResponse(
        tales=tales,
        total=total,
        page=page,
        page_size=page_size
    )

@router.get("/{id}", response_model=TaleDetail)
async def get_tale(
    id: int,
    conn: sqlite3.Connection = Depends(get_db)
):
    row = conn.execute(
        "SELECT id, titulo, origem, url, texto_completo FROM tales WHERE id = ?",
        (id,)
    ).fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Tale not found")
    
    classifications_map = get_classifications_for_tales(conn, [id])
    
    return TaleDetail(
        id=row["id"],
        titulo=row["titulo"],
        origem=row["origem"],
        url=row["url"],
        texto_completo=row["texto_completo"],
        classifications=classifications_map.get(id, [])
    )
