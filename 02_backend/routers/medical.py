"""
AntiGravity Ventures — Medical Sector: FastAPI Router
/api/medical/* endpoints
"""
from __future__ import annotations

import sys
from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal

# Agent path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "04_ai_agents"))
from agents.medical_agent import MedicalAgent  # noqa: E402

router = APIRouter(prefix="/api/medical", tags=["Medical"])
agent = MedicalAgent()


# ---------------------------------------------------------------------------
# Request / Response schemas (router-level, lightweight wrappers)
# ---------------------------------------------------------------------------

class IntakeBody(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., description="International phone format")
    language: Literal["ru", "en", "tr", "th"] = "ru"
    procedure_interest: str = Field(..., min_length=1)
    urgency: Literal["routine", "soon", "urgent", "emergency"] = "routine"
    budget_usd: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = Field(None, max_length=1000)
    referral_source: Optional[str] = None
    phuket_arrival_date: Optional[str] = None

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        cleaned = v.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if not cleaned.startswith("+"):
            cleaned = "+" + cleaned
        if len(cleaned) < 9 or len(cleaned) > 16:
            raise ValueError("Invalid phone number format")
        return cleaned


class StatusUpdateBody(BaseModel):
    patient_id: str
    new_status: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/intake")
def submit_intake(body: IntakeBody) -> dict:
    """
    Yeni hasta başvurusu.
    Prosedür sınıflandırması, hastane eşleştirmesi ve komisyon hesaplaması yapar.
    """
    try:
        result = agent.process_intake(body.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patient/{patient_id}")
def get_patient(patient_id: str) -> dict:
    """Hasta kaydını getirir."""
    record = agent.get_patient(patient_id)
    if not record:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")
    return record


@router.patch("/patient/status")
def update_patient_status(body: StatusUpdateBody) -> dict:
    """Hasta durumunu günceller."""
    return agent.update_status(body.patient_id, body.new_status)


@router.get("/patients")
def list_patients(status: Optional[str] = None) -> dict:
    """Hasta listesi (isteğe bağlı status filtresi)."""
    patients = agent.list_patients(status_filter=status)
    return {"total": len(patients), "patients": patients}


@router.get("/commission/summary")
def commission_summary() -> dict:
    """Komisyon pipeline özetini döndürür."""
    return agent.get_commission_summary()


@router.get("/hospitals")
def list_hospitals() -> dict:
    """Partner hastane listesi."""
    from agents.medical_agent import PARTNER_HOSPITALS
    return {"total": len(PARTNER_HOSPITALS), "hospitals": PARTNER_HOSPITALS}


@router.get("/procedures")
def list_procedures() -> dict:
    """Desteklenen prosedür kategorileri ve tahmini maliyetler."""
    from agents.medical_agent import PROCEDURE_PRICES_USD
    return {
        "categories": [
            {"category": k, "base_price_usd": v, "commission_22pct": round(v * 0.22, 0)}
            for k, v in PROCEDURE_PRICES_USD.items()
        ]
    }
