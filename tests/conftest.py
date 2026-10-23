from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_session
from app.main import app


@pytest.fixture
def session() -> Iterator[Session]:
    """Fresh in-memory SQLite database per test (like RefreshDatabase)."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # one shared connection, so every session sees the same in-memory DB
    )
    Base.metadata.create_all(engine)
    with sessionmaker(bind=engine, expire_on_commit=False)() as db_session:
        yield db_session
    engine.dispose()


@pytest.fixture
def client(session: Session) -> Iterator[TestClient]:
    """HTTP client using the test DB session (like $this->app->instance() in Laravel)."""
    app.dependency_overrides[get_session] = lambda: session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
