import pytest
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Add the project root to Python path
project_root = os.path.join(os.path.dirname(__file__), "..", "..", "..")
sys.path.insert(0, project_root)


@pytest.fixture(scope="session")
def test_engine():
    """Test database engine with in-memory SQLite"""
    from app.policy_management.infrastructure.db import Base
    from app.policy_management.infrastructure.models import PolicyModel

    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture
def db_session(test_engine):
    """Database session for tests"""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(autocommit=False, autoflush=False, bind=connection)()

    try:
        from app.policy_management.infrastructure.seed_data import (
            seed_statuses_and_types,
        )

        seed_statuses_and_types(session)
    except ImportError:
        pass

    yield session
    session.close()
    transaction.rollback()
    connection.close()


# conftest.py (replace the existing client fixture)
import importlib


@pytest.fixture
def client(db_session):
    """Test client - use Starlette TestClient explicitly to avoid ambiguity"""
    # import inside fixture for cleaner import order in tests
    from app.policy_management.api.app_factory import create_app
    from app.policy_management.infrastructure.db import get_db

    # Explicit import from starlette
    from starlette.testclient import TestClient

    app = create_app()
    app.dependency_overrides[get_db] = lambda: db_session

    return TestClient(app)
