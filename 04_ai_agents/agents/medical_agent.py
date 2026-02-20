"""
AntiGravity Ventures — Medical Agent (Full Implementation)
Phuket ↔ Turkey medical tourism referral engine.

Sorumluluklar:
  1. Hasta intake işleme & kayıt
  2. Prosedür kategorisi belirleme
  3. Partner hastane eşleştirme (kural + skor tabanlı)
  4. Komisyon hesaplama & kayıt
  5. Koordinatör mesaj üretme (RU/TR/EN)
  6. Durum takibi
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional
import sys

# Model path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "02_backend"))

logger = logging.getLogger("MedicalAgent")


# ---------------------------------------------------------------------------
# Partner Hospital Registry (gerçekte Firestore'dan gelecek)
# ---------------------------------------------------------------------------

PARTNER_HOSPITALS = [
    {
        "hospital_id": "MEM-IST-001",
        "name": "Memorial Şişli Hastanesi",
        "city": "Istanbul",
        "country": "Turkey",
        "specialties": ["aesthetic", "bariatric", "oncology", "checkup"],
        "commission_rate": 0.22,
        "contact_whatsapp": "+905001234567",
        "avg_procedure_cost_usd": 5_500,
        "rating": 4.8,
        "languages": ["tr", "ru", "en"],
    },
    {
        "hospital_id": "ACI-IST-002",
        "name": "Acıbadem Maslak Hastanesi",
        "city": "Istanbul",
        "country": "Turkey",
        "specialties": ["dental", "checkup", "ophthalmology", "ivf"],
        "commission_rate": 0.20,
        "contact_whatsapp": "+905002345678",
        "avg_procedure_cost_usd": 4_000,
        "rating": 4.9,
        "languages": ["tr", "ru", "en"],
    },
    {
        "hospital_id": "EST-ANT-003",
        "name": "EsteNove Estetik Kliniği",
        "city": "Antalya",
        "country": "Turkey",
        "specialties": ["aesthetic", "hair", "dermatology"],
        "commission_rate": 0.25,
        "contact_whatsapp": "+905003456789",
        "avg_procedure_cost_usd": 3_500,
        "rating": 4.7,
        "languages": ["tr", "ru", "en", "ar"],
    },
    {
        "hospital_id": "DENT-IST-004",
        "name": "DentGroup Istanbul",
        "city": "Istanbul",
        "country": "Turkey",
        "specialties": ["dental"],
        "commission_rate": 0.22,
        "contact_whatsapp": "+905004567890",
        "avg_procedure_cost_usd": 2_000,
        "rating": 4.6,
        "languages": ["tr", "ru", "en", "de"],
    },
    {
        "hospital_id": "HAIR-IST-005",
        "name": "HairCure Istanbul",
        "city": "Istanbul",
        "country": "Turkey",
        "specialties": ["hair"],
        "commission_rate": 0.25,
        "contact_whatsapp": "+905005678901",
        "avg_procedure_cost_usd": 3_000,
        "rating": 4.7,
        "languages": ["tr", "ru", "en"],
    },
]

# Prosedür → kategori mapping
PROCEDURE_CATEGORY_MAP: dict[str, str] = {
    "rhinoplasty": "aesthetic", "rinoplasti": "aesthetic", "burun": "aesthetic",
    "liposuction": "aesthetic", "abdominoplasty": "aesthetic", "karın germe": "aesthetic",
    "göğüs": "aesthetic", "breast": "aesthetic",
    "hair transplant": "hair", "saç ekimi": "hair", "hair": "hair",
    "dental": "dental", "diş": "dental", "implant": "dental",
    "veneer": "dental", "kaplama": "dental", "zirkon": "dental",
    "skin": "dermatology", "cilt": "dermatology", "lazer": "dermatology",
    "checkup": "checkup", "check-up": "checkup", "tahlil": "checkup",
    "eye": "ophthalmology", "göz": "ophthalmology", "lasik": "ophthalmology",
    "bariatric": "bariatric", "obezite": "bariatric", "gastrik": "bariatric",
    "ivf": "ivf", "tüp bebek": "ivf",
    "cancer": "oncology", "kanser": "oncology", "tümör": "oncology",
}

# Prosedür → baz fiyat (USD)
PROCEDURE_PRICES_USD: dict[str, float] = {
    "aesthetic": 5_500,
    "hair": 3_000,
    "dental": 2_000,
    "dermatology": 1_200,
    "checkup": 600,
    "ophthalmology": 2_500,
    "bariatric": 7_500,
    "ivf": 4_500,
    "oncology": 8_000,
    "other": 3_000,
}

# Koordinatör mesajlar (lokalizasyon)
COORDINATOR_MESSAGES: dict[str, str] = {
    "ru": (
        "Здравствуйте! 🏥\n\n"
        "Ваша заявка получена в AntiGravity Medical Phuket.\n"
        "Наш координатор свяжется с вами в течение **5 минут** через WhatsApp.\n\n"
        "📋 Заявка: #{patient_id}\n"
        "🏨 Рекомендуемая клиника: {hospital}\n"
        "💰 Предварительная стоимость: ${cost:,.0f} USD\n\n"
        "Пожалуйста, подготовьте фото паспорта и медицинские документы."
    ),
    "en": (
        "Hello! 🏥\n\n"
        "Your inquiry has been received by AntiGravity Medical Phuket.\n"
        "Our coordinator will contact you within **5 minutes** via WhatsApp.\n\n"
        "📋 Reference: #{patient_id}\n"
        "🏨 Recommended clinic: {hospital}\n"
        "💰 Estimated cost: ${cost:,.0f} USD\n\n"
        "Please prepare a passport photo and any medical records."
    ),
    "tr": (
        "Merhaba! 🏥\n\n"
        "Başvurunuz AntiGravity Medical Phuket tarafından alındı.\n"
        "Koordinatörümüz **5 dakika** içinde WhatsApp'tan sizinle iletişime geçecek.\n\n"
        "📋 Referans: #{patient_id}\n"
        "🏨 Önerilen klinik: {hospital}\n"
        "💰 Tahmini maliyet: ${cost:,.0f} USD\n\n"
        "Pasaport fotoğrafı ve tıbbi belgelerinizi hazırlayınız."
    ),
}


# ---------------------------------------------------------------------------
# Medical Agent
# ---------------------------------------------------------------------------

class MedicalAgent:
    """
    ThaiTurk Medical Tourism Referral Agent.
    Her hasta talebini end-to-end yönetir.
    """

    def __init__(self) -> None:
        self._patient_db: dict[str, dict] = {}   # Stub — Firestore ile replace edilecek
        logger.info("MedicalAgent initialized — Phuket↔Turkey referral engine active.")

    # ----------------------------------------------------------------
    # Public API
    # ----------------------------------------------------------------

    def process_intake(self, intake_data: dict) -> dict:
        """
        Yeni hasta başvurusu işler.
        Returns: IntakeResponse dict
        """
        patient_id = self._generate_patient_id()
        logger.info(f"[MedicalAgent] Processing new intake: {patient_id}")

        # 1. Prosedür kategorisi belirle
        procedure_text = intake_data.get("procedure_interest", "")
        category = self._classify_procedure(procedure_text)
        intake_data["procedure_category"] = category

        # 2. Hastane eşleştir
        hospital = self._match_hospital(category, intake_data.get("language", "ru"))

        # 3. Maliyet & komisyon hesapla
        budget = intake_data.get("budget_usd")
        cost = self._estimate_cost(category, budget)
        commission_rate = hospital.get("commission_rate", 0.22) if hospital else 0.22
        commission = round(cost * commission_rate, 2)

        # 4. Hasta kaydı oluştur
        record = {
            "patient_id": patient_id,
            "intake": intake_data,
            "status": "inquiry",
            "matched_hospital": hospital.get("hospital_id") if hospital else None,
            "estimated_procedure_cost_usd": cost,
            "commission_rate": commission_rate,
            "commission_usd": commission,
            "created_at": datetime.utcnow().isoformat(),
            "tags": self._generate_tags(intake_data, category),
        }
        self._patient_db[patient_id] = record
        logger.info(f"[MedicalAgent] Patient {patient_id} registered → {category} → {hospital.get('name') if hospital else 'No match'}")

        # 5. Koordinatör mesajı üret
        lang = intake_data.get("language", "ru")
        coordinator_msg = self._generate_coordinator_message(
            patient_id=patient_id,
            hospital_name=hospital.get("name", "N/A") if hospital else "TBD",
            cost=cost,
            language=lang,
        )

        # 6. Sonraki adımlar
        next_steps = self._build_next_steps(category, hospital, intake_data)

        return {
            "success": True,
            "patient_id": patient_id,
            "procedure_category": category,
            "message": "Başvuru alındı. Koordinatör 5 dakika içinde iletişime geçecek.",
            "matched_hospital": hospital,
            "estimated_procedure_cost_usd": cost,
            "commission_rate_pct": f"{commission_rate:.0%}",
            "commission_usd": commission,
            "next_steps": next_steps,
            "coordinator_message": coordinator_msg,
            "record": record,
        }

    def get_patient(self, patient_id: str) -> Optional[dict]:
        """Hasta kaydını getirir."""
        return self._patient_db.get(patient_id)

    def update_status(self, patient_id: str, new_status: str) -> dict:
        """Hasta durumunu günceller."""
        if patient_id not in self._patient_db:
            return {"error": f"Patient {patient_id} not found"}
        self._patient_db[patient_id]["status"] = new_status
        self._patient_db[patient_id]["updated_at"] = datetime.utcnow().isoformat()
        logger.info(f"[MedicalAgent] {patient_id} status → {new_status}")
        return {"success": True, "patient_id": patient_id, "status": new_status}

    def list_patients(self, status_filter: Optional[str] = None) -> list[dict]:
        """Tüm hastaları listeler, isteğe bağlı status filtresiyle."""
        patients = list(self._patient_db.values())
        if status_filter:
            patients = [p for p in patients if p.get("status") == status_filter]
        return patients

    def get_commission_summary(self) -> dict:
        """Tüm komisyon özetini döndürür."""
        total_confirmed = sum(
            p.get("commission_usd", 0)
            for p in self._patient_db.values()
            if p.get("status") in ("treatment_confirmed", "completed")
        )
        total_pending = sum(
            p.get("commission_usd", 0)
            for p in self._patient_db.values()
            if p.get("status") in ("inquiry", "consultation_scheduled", "hospital_matched")
        )
        return {
            "total_patients": len(self._patient_db),
            "confirmed_commission_usd": round(total_confirmed, 2),
            "pending_commission_usd": round(total_pending, 2),
            "total_pipeline_usd": round(total_confirmed + total_pending, 2),
        }

    # ----------------------------------------------------------------
    # Private Helpers
    # ----------------------------------------------------------------

    def _classify_procedure(self, text: str) -> str:
        text_lower = text.lower()
        for keyword, category in PROCEDURE_CATEGORY_MAP.items():
            if keyword in text_lower:
                return category
        return "other"

    def _match_hospital(self, category: str, language: str) -> Optional[dict]:
        """Kategoriye ve dile göre en iyi hastaneyi seç."""
        candidates = [
            h for h in PARTNER_HOSPITALS
            if category in h.get("specialties", [])
        ]
        if not candidates:
            candidates = PARTNER_HOSPITALS   # Fallback: tümünü değerlendir

        # Skorlama: dil uyumu + rating + commission_rate
        def score(h: dict) -> float:
            lang_bonus = 0.5 if language in h.get("languages", []) else 0.0
            return h.get("rating", 4.0) + lang_bonus - h.get("commission_rate", 0.22)

        best = max(candidates, key=score)
        logger.info(f"[MedicalAgent] Hospital matched: {best['name']} (score={score(best):.2f})")
        return best

    def _estimate_cost(self, category: str, budget: Optional[float]) -> float:
        base = PROCEDURE_PRICES_USD.get(category, 3_000)
        if budget and budget > 0:
            return min(budget, base * 1.2)  # Budget eğer makul aralıktaysa kullan
        return base

    def _generate_coordinator_message(
        self, patient_id: str, hospital_name: str, cost: float, language: str
    ) -> str:
        template = COORDINATOR_MESSAGES.get(language, COORDINATOR_MESSAGES["en"])
        return template.format(
            patient_id=patient_id,
            hospital=hospital_name,
            cost=cost,
        )

    def _generate_tags(self, intake: dict, category: str) -> list[str]:
        tags = [category, intake.get("urgency", "routine"), intake.get("language", "ru")]
        if intake.get("budget_usd") and intake["budget_usd"] > 5_000:
            tags.append("high-value")
        if intake.get("urgency") in ("urgent", "emergency"):
            tags.append("priority")
        return [t for t in tags if t]

    def _build_next_steps(self, category: str, hospital: Optional[dict], intake: dict) -> list[str]:
        steps = [
            "📱 Koordinatör WhatsApp üzerinden iletişime geçecek (5 dk)",
            "📋 Phuket'te ön konsültasyon randevusu planlanacak",
        ]
        if category in ("aesthetic", "bariatric", "oncology"):
            steps.append("🩺 Mevcut tıbbi belgeler talep edilecek (kan tahlili, görüntüleme)")
        steps.append(f"✈️ Türkiye ({hospital.get('city', 'Istanbul') if hospital else 'Istanbul'}) transfer organizasyonu")
        steps.append("💰 Kesin fiyat teklifi ve ödeme planı sunulacak")
        if intake.get("phuket_arrival_date"):
            steps.append(f"📅 Geliş tarihi: {intake['phuket_arrival_date']} — takvim güncellendi")
        return steps

    @staticmethod
    def _generate_patient_id() -> str:
        return f"MED-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:6].upper()}"
