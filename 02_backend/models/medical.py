"""
AntiGravity Ventures — Medical Sector: Pydantic v2 Data Models
Hasta profili, prosedür talebi, referral kaydı ve komisyon modelleri.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Language(str, Enum):
    RU = "ru"
    TR = "tr"
    EN = "en"
    TH = "th"


class PatientStatus(str, Enum):
    INQUIRY = "inquiry"            # İlk temas
    CONSULTATION_SCHEDULED = "consultation_scheduled"
    DOCS_REQUESTED = "docs_requested"
    HOSPITAL_MATCHED = "hospital_matched"
    TREATMENT_CONFIRMED = "treatment_confirmed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class ProcedureCategory(str, Enum):
    AESTHETIC = "aesthetic"        # Estetik / plastik cerrahi
    HAIR = "hair"                  # Saç ekimi
    DENTAL = "dental"              # Diş hekimliği
    DERMATOLOGY = "dermatology"    # Dermatoloji
    CHECKUP = "checkup"            # Genel check-up
    OPHTHALMOLOGY = "ophthalmology" # Göz
    BARIATRIC = "bariatric"        # Obezite cerrahisi
    IVF = "ivf"                    # Tüp bebek
    ONCOLOGY = "oncology"          # Onkoloji (konsültasyon)
    OTHER = "other"


class UrgencyLevel(str, Enum):
    ROUTINE = "routine"            # 4+ hafta
    SOON = "soon"                  # 1-4 hafta
    URGENT = "urgent"              # 1 hafta içinde
    EMERGENCY = "emergency"        # Acil


# ---------------------------------------------------------------------------
# Patient Intake
# ---------------------------------------------------------------------------

class PatientIntakeRequest(BaseModel):
    """Hasta ilk başvuru formu."""
    full_name: str = Field(..., min_length=2, max_length=100, description="Hasta tam adı")
    phone: str = Field(..., description="WhatsApp/telefon (uluslararası format: +66...)")
    language: Language = Field(Language.RU, description="İletişim dili")
    procedure_interest: str = Field(..., description="İlgilenilen prosedür (serbest metin)")
    procedure_category: Optional[ProcedureCategory] = Field(None)
    urgency: UrgencyLevel = Field(UrgencyLevel.ROUTINE)
    budget_usd: Optional[float] = Field(None, ge=0)
    notes: Optional[str] = Field(None, max_length=1000)
    referral_source: Optional[str] = Field(None, description="Bizi nereden duydunuz?")
    phuket_arrival_date: Optional[str] = Field(None, description="Phuket'e geliş tarihi YYYY-MM-DD")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        cleaned = v.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        if not cleaned.startswith("+"):
            cleaned = "+" + cleaned
        if len(cleaned) < 9 or len(cleaned) > 16:
            raise ValueError("Geçersiz telefon numarası formatı")
        return cleaned


class PatientRecord(BaseModel):
    """Sistem içi tam hasta kaydı."""
    patient_id: str
    intake: PatientIntakeRequest
    status: PatientStatus = PatientStatus.INQUIRY
    assigned_coordinator: Optional[str] = None
    matched_hospital: Optional[str] = None
    matched_doctor: Optional[str] = None
    estimated_procedure_cost_usd: Optional[float] = None
    commission_usd: Optional[float] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    consultation_date: Optional[str] = None
    tags: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Hospital & Doctor
# ---------------------------------------------------------------------------

class PartnerHospital(BaseModel):
    hospital_id: str
    name: str
    city: str
    country: str = "Turkey"
    specialties: list[ProcedureCategory]
    commission_rate: float = Field(0.22, ge=0, le=0.5)
    contact_email: Optional[str] = None
    contact_whatsapp: Optional[str] = None
    avg_procedure_cost_usd: Optional[float] = None
    rating: float = Field(4.5, ge=0, le=5)
    languages: list[Language] = Field(default_factory=lambda: [Language.TR, Language.EN, Language.RU])


# ---------------------------------------------------------------------------
# API Responses
# ---------------------------------------------------------------------------

class IntakeResponse(BaseModel):
    success: bool
    patient_id: str
    message: str
    matched_hospital: Optional[PartnerHospital] = None
    estimated_commission_usd: Optional[float] = None
    next_steps: list[str] = Field(default_factory=list)
    coordinator_message: Optional[str] = None   # Rusça/İngilizce otomatik mesaj


class CommissionRecord(BaseModel):
    record_id: str
    patient_id: str
    hospital_id: str
    procedure: str
    procedure_cost_usd: float
    commission_rate: float
    commission_usd: float
    status: str = "pending"   # pending | confirmed | paid
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
