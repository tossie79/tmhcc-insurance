"""
Main entry point for the application - run from project root
"""

import uvicorn
from app.policy_management.api.app_factory import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
