"""Templates initialization module to avoid circular imports."""

from pathlib import Path
from fastapi.templating import Jinja2Templates

# Define templates directory
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "xer" / "templates"

# Initialize Jinja2 templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
