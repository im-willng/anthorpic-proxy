from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pathlib import Path

router = APIRouter(tags=["admin"])

# Get the path to templates directory
templates_dir = Path(__file__).parent.parent.parent / "templates"


@router.get("/admin", response_class=HTMLResponse)
def get_admin_page():
    """Serve the admin dashboard page."""
    admin_html = templates_dir / "admin.html"
    if admin_html.exists():
        return admin_html.read_text()
    return "<h1>Admin page not found</h1>"
