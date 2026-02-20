"""
AntiGravity Ventures — ThaiTurk Backend
FastAPI entry point.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pathlib import Path
import sys

# Add parent to path so agents module is importable
sys.path.insert(0, str(Path(__file__).parent.parent / "04_ai_agents"))
from master_orchestrator import AgentRouter  # noqa: E402

app = FastAPI(
    title="AntiGravity ThaiTurk API",
    description="Medical · Travel · Factory — AI-powered routing platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

router = AgentRouter()


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
    return router.route({"message": req.message, "language": req.language})


@app.get("/api/sectors")
def sectors() -> dict:
    return {
        "sectors": ["Medical", "Travel", "Factory"],
        "active": ["Medical", "Travel"],
        "dormant": ["Factory"],
    }
