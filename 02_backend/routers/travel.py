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

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field, model_validator
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import TravelRequest as TravelRequestModel

import logging
logger = logging.getLogger("thaiturk.travel")

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
    language: Literal["ru", "en", "tr", "th", "ar", "zh"] = "en"
    destination: Optional[str] = None
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    guests: Optional[int] = Field(default=2, ge=1, le=20)
    notes: Optional[str] = Field(None, max_length=1000)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.check_in and self.check_out and self.check_out <= self.check_in:
            raise ValueError("check_out must be after check_in")
        return self


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/options")
def travel_options(body: TravelRequestBody, request: Request, db: Session = Depends(get_db)) -> dict:
    """
    Seyahat talebi al ve TravelAgent üzerinden destinasyon/otel önerisi üret.
    """
    request_id = f"TRV-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    # Persist travel request to DB
    from datetime import date as date_type
    check_in_date = None
    check_out_date = None
    if body.check_in:
        try:
            check_in_date = date_type.fromisoformat(body.check_in)
        except (ValueError, TypeError):
            pass
    if body.check_out:
        try:
            check_out_date = date_type.fromisoformat(body.check_out)
        except (ValueError, TypeError):
            pass

    try:
        travel_req = TravelRequestModel(
            request_id=request_id,
            full_name=body.full_name,
            phone=body.phone,
            language=body.language,
            destination=body.destination or "Phuket",
            check_in=check_in_date,
            check_out=check_out_date,
            guests=body.guests,
            notes=body.notes,
        )
        db.add(travel_req)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to persist travel request: {e}")
        raise HTTPException(status_code=500, detail="Failed to save travel request")

    # Route through TravelAgent
    try:
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
    except Exception as e:
        logger.error(f"TravelAgent error: {e}")
        result = {}

    return {
        "request_id": request_id,
        "status": "received",
        "coordinator_message": result.get("coordinator_message", ""),
        "suggestions": result.get("suggestions", []),
        "next_steps": result.get("next_steps", [
            "Coordinator contacts you via WhatsApp (5 min)",
            "Hotel options forwarded",
            "Dates confirmed & booking arranged",
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
