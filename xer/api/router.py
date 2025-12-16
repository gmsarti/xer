"""Main API router that combines all sub-routers."""

from fastapi import APIRouter, Request, status
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, JSONResponse

from xer.templates_config import templates
from xer.database import list_tales

# Import sub-routers
from . import tales as tales_router

router = APIRouter()

# Include sub-routers with proper prefixes
router.include_router(tales_router.router, prefix="/api/v1", tags=["tales"])


@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request) -> HTMLResponse:
    """Render the homepage with a list of tales.

    Args:
        request: FastAPI request object

    Returns:
        Rendered HTML template
    """
    tales = list_tales(limit=20, offset=0)
    return templates.TemplateResponse(
        "index.html", {"request": request, "tales": tales}
    )


@router.get("/tales/{tale_id}", response_class=HTMLResponse)
async def tale_detail(request: Request, tale_id: int) -> HTMLResponse:
    """Render the tale detail page optimized for reading.

    Args:
        request: FastAPI request object
        tale_id: ID of the tale to display

    Returns:
        Rendered HTML template
    """
    from xer.database import get_tale

    tale = get_tale(tale_id)
    if not tale:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "tales": [], "error": "Conto não encontrado"},
            status_code=404,
        )

    return templates.TemplateResponse("tale.html", {"request": request, "tale": tale})


@router.get(
    "/api/v1/hello", response_class=JSONResponse, status_code=status.HTTP_200_OK
)
async def hello_world() -> dict[str, str]:
    """Simple *Hello World* endpoint.

    Returns a JSON payload with a friendly greeting.  The function is async
    to follow FastAPI best‑practice recommendations for non‑blocking I/O.
    """
    return {"message": "Hello, World!"}


@router.get("/health", response_class=JSONResponse, status_code=status.HTTP_200_OK)
async def health_check() -> dict[str, str]:
    """Health‑check endpoint used by orchestration tools.

    Returns a minimal JSON payload indicating that the service is alive.
    """
    return {"status": "ok"}


# New input validation model
class EchoRequest(BaseModel):
    """Schema for echo endpoint request body.

    Fields:
        message: The text that will be echoed back.
    """

    message: str


@router.post("/echo", response_class=JSONResponse, status_code=status.HTTP_200_OK)
async def echo(request: EchoRequest) -> dict[str, str]:
    """Echo endpoint that validates input with Pydantic.

    Returns the same message received in the request body.
    """
    return {"echo": request.message}
