from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

# Set up Jinja2 templates directory
current_dir = os.path.dirname(__file__)
templates_dir = os.path.join(current_dir, "..", "templates")
templates = Jinja2Templates(directory=templates_dir)

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):
    """Serve the main frontend dashboard"""
    return templates.TemplateResponse("index.html", {"request": request})
