from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .config import get_settings

settings = get_settings()

# Check that the directories exist
settings.static_dir.mkdir(exist_ok=True)
settings.templates_dir.mkdir(exist_ok=True)

# Create templates instance
templates = Jinja2Templates(directory=str(settings.templates_dir))


def setup_static_files(app: FastAPI):
    """Setup static files and templates"""
    app.mount("/static", StaticFiles(directory=str(settings.static_dir)), name="static")
