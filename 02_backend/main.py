"""
AntiGravity Ventures — ThaiTurk Backend
FastAPI entry point.
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database.connection import Base, engine
from database import models  # noqa: F401  — register all ORM models

logger = logging.getLogger("thaiturk")

# Try to import AgentRouter from 04_ai_agents (local dev / Railway monorepo)
_agents_path = Path(__file__).parent.parent / "04_ai_agents"
if _agents_path.exists():
    sys.path.insert(0, str(_agents_path))

try:
    from master_orchestrator import AgentRouter  # noqa: E402
except ImportError:
    # Fallback stub when 04_ai_agents isn't available (e.g. isolated deployment)
    class AgentRouter:
        def route(self, payload: dict) -> dict:
            return {"status": "ok", "message": "Orchestrator not available", "payload": payload}


from routers.medical import router as medical_router  # noqa: E402
from routers.travel import router as travel_router  # noqa: E402
from routers.marketing import router as marketing_router  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup (dev convenience). Alembic handles prod migrations."""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables ready.")
    yield


app = FastAPI(
    title="AntiGravity ThaiTurk API",
    description="Medical · Travel · Factory · Marketing — AI-powered routing platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

orchestrator = AgentRouter()

# Register routers
app.include_router(medical_router)
app.include_router(travel_router)
app.include_router(marketing_router)


class InboundRequest(BaseModel):
    message: str
    language: str | None = None
    metadata: dict | None = None


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": "1.0.0"}


@app.post("/api/classify")
def classify(req: InboundRequest) -> dict:
    """Gelen talebi sınıflandır ve ilgili agent'a yönlendir."""
    return orchestrator.route({"message": req.message, "language": req.language})


@app.get("/api/sectors")
def sectors() -> dict:
    return {
        "sectors": ["Medical", "Travel", "Factory", "Marketing"],
        "active": ["Medical", "Travel", "Marketing"],
        "dormant": ["Factory"],
    }
