"""
AntiGravity Ventures — ThaiTurk Backend
FastAPI entry point.
"""
from __future__ import annotations

import logging
import os
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
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables ready.")
    except Exception as e:
        logger.warning(f"Database init skipped: {e}")
    yield


app = FastAPI(
    title="AntiGravity ThaiTurk API",
    description="Medical · Travel · Factory · Marketing — AI-powered routing platform",
    version="1.1.0",
    lifespan=lifespan,
)

_origins = os.getenv("ALLOWED_ORIGINS", "*")
_origin_list = ["*"] if _origins == "*" else [o.strip() for o in _origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origin_list,
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
    return {"status": "ok", "version": "1.1.0"}


@app.post("/api/classify")
def classify(req: InboundRequest) -> dict:
    """Gelen talebi sınıflandır ve ilgili agent'a yönlendir."""
    return orchestrator.route({"message": req.message, "language": req.language})


@app.post("/api/admin/seed")
def run_seed(secret: str = "") -> dict:
    """One-time DB seeder — requires ADMIN_SECRET or ENVIRONMENT != production."""
    import os
    admin_secret = os.getenv("ADMIN_SECRET", "antigravity-seed-2026")
    env = os.getenv("ENVIRONMENT", "development")
    if env == "production" and secret != admin_secret:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="Forbidden")
    from database.seed import seed_hospitals, seed_demo_patients
    from database.connection import SessionLocal
    session = SessionLocal()
    try:
        h = seed_hospitals(session)
        p = seed_demo_patients(session)
        return {"hospitals_seeded": h, "patients_seeded": p}
    finally:
        session.close()


@app.get("/api/sectors")
def sectors() -> dict:
    return {
        "sectors": ["Medical", "Travel", "Factory", "Marketing"],
        "active": ["Medical", "Travel", "Marketing"],
        "dormant": ["Factory"],
    }
