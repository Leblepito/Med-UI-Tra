"""
AntiGravity ThaiTurk — Demo Data Seed Script
Populates in-memory / local storage with realistic demo records.
Run: python 03_data/seeds/demo_data.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

# ─── Paths ───────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent.parent

# Allow importing agents directly
sys.path.insert(0, str(ROOT / "04_ai_agents"))

from agents.medical_agent import MedicalAgent  # noqa: E402
from agents.travel_agent import TravelAgent      # noqa: E402


# ─── Demo Patients ────────────────────────────────────────────────────────────
DEMO_PATIENTS = [
    {"full_name": "Elena Petrova",   "phone": "+79001234567", "language": "ru", "procedure_interest": "Ринопластика",        "urgency": "soon",    "budget_usd": 4000},
    {"full_name": "James Wilson",    "phone": "+447700900100", "language": "en", "procedure_interest": "Hair Transplant",     "urgency": "routine", "budget_usd": 3500},
    {"full_name": "Ayse Yilmaz",     "phone": "+905321234567", "language": "tr", "procedure_interest": "Saç Ekimi",           "urgency": "routine", "budget_usd": 2500},
    {"full_name": "Maria Ivanova",   "phone": "+79009876543", "language": "ru", "procedure_interest": "Стоматология/Виниры", "urgency": "soon",    "budget_usd": 2000},
    {"full_name": "Mehmet Demir",    "phone": "+905001234567", "language": "tr", "procedure_interest": "Göz Ameliyatı",       "urgency": "urgent",  "budget_usd": 3000},
]

# ─── Demo Travel Requests ─────────────────────────────────────────────────────
DEMO_TRAVEL = [
    {"full_name": "Sergei Volkov",   "phone": "+79001111111", "language": "ru", "destination": "Phuket — Patong Beach", "guests": 2, "check_in": "2026-03-15"},
    {"full_name": "Anna Williams",   "phone": "+447700111222", "language": "en", "destination": "Krabi",                 "guests": 4, "check_in": "2026-04-01"},
]


def seed_patients(agent: MedicalAgent) -> None:
    print("\n🏥 Seeding demo patients...")
    for p in DEMO_PATIENTS:
        result = agent.process_intake(p)
        print(f"  ✓ {p['full_name']} → {result.get('matched_hospital', {}).get('name', '?')} [{result.get('patient_id')}]")


def seed_travel(agent: TravelAgent) -> None:
    print("\n🏖️  Seeding demo travel requests...")
    import uuid
    for t in DEMO_TRAVEL:
        req_id = f"TRV-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        result = agent.process_request({**t, "request_id": req_id})
        print(f"  ✓ {t['full_name']} → {t['destination']} [{req_id}]")


def main() -> None:
    print("=" * 55)
    print("  AntiGravity ThaiTurk — Demo Data Seed")
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 55)

    medical_agent = MedicalAgent()
    travel_agent = TravelAgent()

    seed_patients(medical_agent)
    seed_travel(travel_agent)

    print("\n✅ Seed complete!\n")


if __name__ == "__main__":
    main()
