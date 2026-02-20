"""
AntiGravity Ventures — Database Seeder
Populates hospitals from PARTNER_HOSPITALS + demo patients.

Usage:
    cd 02_backend
    python -m database.seed
"""
from __future__ import annotations

import sys
import uuid
from datetime import datetime
from pathlib import Path

# Ensure backend root is on path
sys.path.insert(0, str(Path(__file__).parent.parent))

from database.connection import Base, engine, SessionLocal
from database.models import Hospital, Patient

# Import hospital data from medical agent
_agents_path = Path(__file__).parent.parent.parent / "04_ai_agents"
sys.path.insert(0, str(_agents_path))
from agents.medical_agent import PARTNER_HOSPITALS  # noqa: E402


def seed_hospitals(session) -> int:
    """Insert partner hospitals if not already present."""
    count = 0
    for h in PARTNER_HOSPITALS:
        existing = session.get(Hospital, h["hospital_id"])
        if existing:
            continue
        hospital = Hospital(
            hospital_id=h["hospital_id"],
            name=h["name"],
            city=h["city"],
            country=h.get("country", "Turkey"),
            specialties=h["specialties"],
            commission_rate=h.get("commission_rate", 0.22),
            contact_whatsapp=h.get("contact_whatsapp"),
            avg_procedure_cost_usd=h.get("avg_procedure_cost_usd"),
            rating=h.get("rating", 4.5),
            languages=h.get("languages", ["tr", "en"]),
            jci_accredited=h.get("jci_accredited", False),
            active=True,
        )
        session.add(hospital)
        count += 1
    session.commit()
    return count


def seed_demo_patients(session) -> int:
    """Insert a few demo patients for testing."""
    demos = [
        {
            "full_name": "Dmitri Petrov",
            "phone": "+79001234567",
            "language": "ru",
            "procedure_interest": "hair transplant",
            "procedure_category": "hair",
            "urgency": "routine",
            "budget_usd": 4000,
            "status": "inquiry",
            "matched_hospital_id": "HAIR-IST-005",
            "estimated_procedure_cost_usd": 3000,
            "commission_rate": 0.25,
            "commission_usd": 750,
            "tags": ["hair", "routine", "ru"],
        },
        {
            "full_name": "Svetlana Ivanova",
            "phone": "+79009876543",
            "language": "ru",
            "procedure_interest": "rhinoplasty",
            "procedure_category": "aesthetic",
            "urgency": "soon",
            "budget_usd": 7000,
            "status": "consultation_scheduled",
            "matched_hospital_id": "MEM-IST-001",
            "estimated_procedure_cost_usd": 5500,
            "commission_rate": 0.22,
            "commission_usd": 1210,
            "tags": ["aesthetic", "soon", "ru", "high-value"],
        },
        {
            "full_name": "Ahmed Al-Rashid",
            "phone": "+971501234567",
            "language": "en",
            "procedure_interest": "dental veneers",
            "procedure_category": "dental",
            "urgency": "routine",
            "budget_usd": 3000,
            "status": "hospital_matched",
            "matched_hospital_id": "DENT-IST-004",
            "estimated_procedure_cost_usd": 2000,
            "commission_rate": 0.22,
            "commission_usd": 440,
            "tags": ["dental", "routine", "en"],
        },
        {
            "full_name": "Elif Yilmaz",
            "phone": "+905551234567",
            "language": "tr",
            "procedure_interest": "gastric sleeve",
            "procedure_category": "bariatric",
            "urgency": "urgent",
            "budget_usd": 10000,
            "status": "treatment_confirmed",
            "matched_hospital_id": "MEM-IST-001",
            "estimated_procedure_cost_usd": 7500,
            "commission_rate": 0.22,
            "commission_usd": 1650,
            "tags": ["bariatric", "urgent", "tr", "high-value", "priority"],
        },
        {
            "full_name": "Olga Smirnova",
            "phone": "+79007654321",
            "language": "ru",
            "procedure_interest": "skin laser treatment",
            "procedure_category": "dermatology",
            "urgency": "routine",
            "budget_usd": 1500,
            "status": "completed",
            "matched_hospital_id": "EST-ANT-003",
            "estimated_procedure_cost_usd": 1200,
            "commission_rate": 0.25,
            "commission_usd": 300,
            "tags": ["dermatology", "routine", "ru"],
        },
    ]

    count = 0
    for d in demos:
        pid = f"MED-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        existing = session.query(Patient).filter_by(full_name=d["full_name"]).first()
        if existing:
            continue
        patient = Patient(
            patient_id=pid,
            full_name=d["full_name"],
            phone=d["phone"],
            language=d["language"],
            procedure_interest=d["procedure_interest"],
            procedure_category=d["procedure_category"],
            urgency=d["urgency"],
            budget_usd=d.get("budget_usd"),
            status=d["status"],
            matched_hospital_id=d.get("matched_hospital_id"),
            estimated_procedure_cost_usd=d.get("estimated_procedure_cost_usd"),
            commission_rate=d.get("commission_rate"),
            commission_usd=d.get("commission_usd"),
            tags=d.get("tags", []),
        )
        session.add(patient)
        count += 1
    session.commit()
    return count


def main() -> None:
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        h_count = seed_hospitals(session)
        print(f"Seeded {h_count} hospitals.")

        p_count = seed_demo_patients(session)
        print(f"Seeded {p_count} demo patients.")

        print("Done!")
    finally:
        session.close()


if __name__ == "__main__":
    main()
