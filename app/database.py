from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

# SQLite connections are bound to one thread by default;
# FastAPI runs sync endpoints in a thread pool.
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

engine = create_engine(settings.database_url, connect_args=connect_args)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_session() -> Iterator[Session]:
    """One session per request; closed after the response is sent."""
    with SessionLocal() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
