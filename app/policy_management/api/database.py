from ..infrastructure.db import seed_initial_data


def init_db():
    """Initialize database tables and seed data on startup"""
    print("Starting up application...")
    seed_initial_data()
    print("Database initialized with sample data!")
