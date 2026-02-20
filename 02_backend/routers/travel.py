"""
AntiGravity Ventures — Travel Sector: FastAPI Router
/api/travel/* endpoints
"""
from __future__ import annotations

import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional, Literal

from fastapi import APIRouter
from pydantic import BaseModel, Field

# Agent path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "04_ai_agents"))
from agents.travel_agent import TravelAgent  # noqa: E402

router = APIRouter(prefix="/api/travel", tags=["Travel"])
agent = TravelAgent()


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------

class TravelRequestBody(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., description="International phone format")
    language: Literal["ru", "en", "tr", "th"] = "en"
    destination: Optional[str] = None
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    guests: Optional[int] = Field(default=2, ge=1, le=20)
    notes: Optional[str] = Field(None, max_length=1000)


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/options")
def travel_options(body: TravelRequestBody) -> dict:
    """
    Seyahat talebi al ve TravelAgent üzerinden destinasyon/otel önerisi üret.
    """
    request_id = f"TRV-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    # Route through TravelAgent
    result = agent.process_request({
        "request_id": request_id,
        "full_name": body.full_name,
        "phone": body.phone,
        "language": body.language,
        "destination": body.destination or "Phuket",
        "check_in": body.check_in,
        "check_out": body.check_out,
        "guests": body.guests,
        "notes": body.notes,
    })

    return {
        "request_id": request_id,
        "status": "received",
        "coordinator_message": result.get("coordinator_message", ""),
        "suggestions": result.get("suggestions", []),
        "next_steps": result.get("next_steps", [
            "📱 Coordinator contacts you via WhatsApp (5 min)",
            "🏨 Hotel options forwarded",
            "🗓️ Dates confirmed & booking arranged",
        ]),
    }


@router.get("/destinations")
def list_destinations() -> dict:
    """Desteklenen destinasyon listesi."""
    return {
        "destinations": [
            {"id": "phuket-patong", "name": "Phuket — Patong Beach", "country": "Thailand", "flag": "🇹🇭"},
            {"id": "phuket-kamala", "name": "Phuket — Kamala", "country": "Thailand", "flag": "🇹🇭"},
            {"id": "phuket-kata", "name": "Phuket — Kata", "country": "Thailand", "flag": "🇹🇭"},
            {"id": "samui", "name": "Koh Samui", "country": "Thailand", "flag": "🇹🇭"},
            {"id": "krabi", "name": "Krabi", "country": "Thailand", "flag": "🇹🇭"},
        ]
    }
