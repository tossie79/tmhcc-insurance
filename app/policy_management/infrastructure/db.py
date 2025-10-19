from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

"""Database setup and session management for Policy Management"""

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./policies.db")
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    from . import models

    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


def seed_initial_data():
    """Create tables and seed initial data"""
    create_tables()
    from .seed_data import seed_database

    db = SessionLocal()
    try:
        seed_database(db)
        print("Database initialization complete!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()
