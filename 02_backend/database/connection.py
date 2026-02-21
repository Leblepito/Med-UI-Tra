"""
AntiGravity Ventures — Database Connection
SQLAlchemy 2.0 engine + session factory.
Railway-compatible (DATABASE_URL env var).
"""
from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    pass


def _build_url() -> str:
    """Read DATABASE_URL from env, apply Railway postgres:// fix."""
    url = os.getenv("DATABASE_URL")
    if not url:
        _env = os.getenv("ENVIRONMENT", "development")
        if _env == "production":
            raise RuntimeError("DATABASE_URL environment variable is required in production")
        # Local dev fallback
        url = "postgresql://postgres:postgres@localhost:5432/thaiturk"
    # Railway uses postgres:// but SQLAlchemy 2.0 requires postgresql://
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif url.startswith("postgresql://") and "+psycopg2" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
    return url


DATABASE_URL = _build_url()

_is_production = os.getenv("ENVIRONMENT", "development") == "production"

engine = create_engine(
    DATABASE_URL,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={"sslmode": "require"} if _is_production else {},
    echo=not _is_production,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency — yields a DB session, auto-closes on exit."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
