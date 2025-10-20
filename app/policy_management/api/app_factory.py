from fastapi import FastAPI
from typing import Optional


def create_app(testing: bool = False) -> FastAPI:
    """
    Application factory pattern - creates and configures the FastAPI app

    Args:
        testing: If True, skips database initialization for tests
    """
    # Create FastAPI instance
    app = FastAPI(
        title="TMHCC Underwriting Policy Management API",
        description="API for managing insurance policies with web interface",
        version="1.0.0",
    )

    from .config import get_settings
    from .middleware import setup_middleware
    from .static_files import setup_static_files

    # Setup configuration
    settings = get_settings()

    # Setup middleware (CORS, etc.)
    setup_middleware(app)

    # Setup static files and templates
    setup_static_files(app)

    # Initialize database only if not testing
    if not testing:
        from .database import init_db

        init_db()

    # Import route modules
    from .routes.health import router as health_router
    from .routes.frontend import router as frontend_router
    from .routes.policies import router as policies_router

    # Register all routes
    app.include_router(health_router, tags=["health"])
    app.include_router(frontend_router)  # /policies
    app.include_router(policies_router)  # /api/v1/policies

    return app
