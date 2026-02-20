"""
AntiGravity Ventures — ThaiTurk AI Platform
Master Orchestrator: Request Classification & Routing Engine

Gelen her talebi (text veya JSON) üç sektöre sınıflandırır:
  - Medical  : Sağlık turizmi, hasta yönlendirme, estetik danışmanlık
  - Travel   : Otel, restoran, rezervasyon, turizm
  - Factory  : Tekstil, B2B üretim, fabrika sorguları

Yazar   : AntiGravity Ventures AI Swarm
Versiyon: 1.0.0
Tarih   : 2026-02-20
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Logging — her çalışmaya ait log AGENT_SESSION.log'a eklenir
# ---------------------------------------------------------------------------
LOG_FILE = Path(__file__).parent / "logs" / "AGENT_SESSION.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger("MasterOrchestrator")


# ---------------------------------------------------------------------------
# Sektör Enum'u
# ---------------------------------------------------------------------------
class Sector(str, Enum):
    MEDICAL = "Medical"
    TRAVEL = "Travel"
    FACTORY = "Factory"
    MARKETING = "Marketing"
    UNKNOWN = "Unknown"


# ---------------------------------------------------------------------------
# Sınıflandırma Sonucu
# ---------------------------------------------------------------------------
@dataclass
class ClassificationResult:
    sector: Sector
    confidence: float          # 0.0 – 1.0
    matched_keywords: list[str]
    reasoning: str
    raw_input: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "sector": self.sector.value,
            "confidence": round(self.confidence, 3),
            "matched_keywords": self.matched_keywords,
            "reasoning": self.reasoning,
            "timestamp": self.timestamp,
        }


# ---------------------------------------------------------------------------
# Anahtar Kelime Sözlükleri  (TR + EN + RU)
# ---------------------------------------------------------------------------
KEYWORD_MAPS: dict[Sector, list[str]] = {
    Sector.MEDICAL: [
        # Türkçe
        "sağlık", "hasta", "doktor", "klinik", "ameliyat", "estetik",
        "rinoplasti", "saç ekimi", "diş", "dermatoloji", "check-up",
        "tedavi", "hastane", "cerrahi", "medikal", "tıp", "reçete",
        "muayene", "konsültasyon", "ameliyathane", "anestezi",
        # English
        "medical", "doctor", "clinic", "surgery", "aesthetic", "rhinoplasty",
        "hair transplant", "dental", "dermatology", "health", "treatment",
        "hospital", "patient", "consultation", "procedure", "cosmetic",
        "checkup", "check-up", "wellness", "recovery", "implant",
        # Russian (transliterated)
        "медицинский", "врач", "клиника", "операция", "эстетика",
        "пластика", "зубы", "лечение", "больница", "пациент",
        "процедура", "имплантация", "доктор",
    ],
    Sector.TRAVEL: [
        # Türkçe
        "otel", "rezervasyon", "konaklama", "restoran", "yemek", "menü",
        "tur", "uçuş", "transfer", "oda", "giriş", "çıkış", "fiyat",
        "tatil", "seyahat", "turizm", "plaj", "havuz", "spa",
        "check-in", "check-out", "fatura", "misafir", "kahvaltı",
        # English
        "hotel", "reservation", "booking", "accommodation", "restaurant",
        "food", "menu", "tour", "flight", "transfer", "room", "check-in",
        "check-out", "price", "holiday", "travel", "tourism", "beach",
        "pool", "breakfast", "guest", "reception", "suite", "villa",
        # Russian
        "отель", "бронирование", "проживание", "ресторан", "тур",
        "перелет", "трансфер", "номер", "заезд", "выезд", "цена",
        "отдых", "туризм", "пляж", "бассейн", "завтрак", "гость",
    ],
    Sector.FACTORY: [
        # Türkçe
        "fabrika", "tekstil", "üretim", "imalat", "ihracat", "ithalat",
        "kumaş", "iplik", "dikiş", "konfeksiyon", "toptan", "sipariş",
        "numune", "kalite kontrol", "tedarik", "kapasite", "moc",
        "fob", "cif", "incoterms", "b2b", "teklif",
        # English
        "factory", "textile", "production", "manufacturing", "export",
        "import", "fabric", "yarn", "sewing", "garment", "wholesale",
        "order", "sample", "quality control", "supply chain", "capacity",
        "fob", "cif", "b2b", "quotation", "shipment", "sourcing",
        # Russian
        "завод", "текстиль", "производство", "экспорт", "ткань",
        "нить", "оптовый", "заказ", "образец", "поставка",
    ],
    Sector.MARKETING: [
        # Türkçe
        "reklam", "pazarlama", "seo", "kampanya", "sosyal medya", "içerik",
        "google ads", "facebook ads", "instagram", "blog", "anahtar kelime",
        "trafik", "dönüşüm", "lead", "hedefleme", "bütçe", "analiz",
        "raporlama", "performans", "marka", "dijital", "yayın", "paylaşım",
        # English
        "marketing", "advertising", "campaign", "social media", "content",
        "google ads", "facebook ads", "keyword", "traffic",
        "conversion", "lead generation", "targeting", "budget", "analytics",
        "reporting", "performance", "brand", "digital", "publish", "ad copy",
        # Russian
        "маркетинг", "реклама", "продвижение", "кампания", "соцсети", "контент",
        "ключевые слова", "трафик", "конверсия", "лид", "таргетинг", "бюджет",
        "аналитика", "отчет", "бренд", "публикация",
    ],
}


# ---------------------------------------------------------------------------
# Classifier
# ---------------------------------------------------------------------------
class RequestClassifier:
    """Kural tabanlı + skor ağırlıklı sektör sınıflandırıcı."""

    def __init__(self) -> None:
        # Compile regex patterns for speed
        self._patterns: dict[Sector, list[re.Pattern[str]]] = {
            sector: [
                re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE | re.UNICODE)
                for kw in keywords
            ]
            for sector, keywords in KEYWORD_MAPS.items()
        }

    def classify(self, text: str) -> ClassificationResult:
        """
        Metni analiz eder ve sektör sınıflandırması döndürür.

        Args:
            text: Ham kullanıcı girdisi (herhangi bir dilde).

        Returns:
            ClassificationResult with sector, confidence and reasoning.
        """
        text_clean = text.strip()
        scores: dict[Sector, float] = {}
        matched: dict[Sector, list[str]] = {}

        for sector, patterns in self._patterns.items():
            hits: list[str] = []
            for i, pattern in enumerate(patterns):
                if pattern.search(text_clean):
                    hits.append(KEYWORD_MAPS[sector][i])
            score = len(hits) / max(len(patterns), 1)
            scores[sector] = score
            matched[sector] = hits

        best_sector = max(scores, key=lambda s: scores[s])
        best_score = scores[best_sector]

        if best_score == 0.0:
            result_sector = Sector.UNKNOWN
            confidence = 0.0
            reasoning = "Hiçbir sektör anahtar kelimesiyle eşleşme bulunamadı. Manuel sınıflandırma gerekebilir."
        else:
            result_sector = best_sector
            confidence = min(best_score * 10, 1.0)   # normalize to [0,1]
            reasoning = (
                f"{best_sector.value} sektörü için "
                f"{len(matched[best_sector])} anahtar kelime eşleşti: "
                f"{', '.join(matched[best_sector][:5])}."
            )

        return ClassificationResult(
            sector=result_sector,
            confidence=confidence,
            matched_keywords=matched.get(result_sector, []),
            reasoning=reasoning,
            raw_input=text_clean,
        )


# ---------------------------------------------------------------------------
# Agent Router
# ---------------------------------------------------------------------------
class AgentRouter:
    """Sınıflandırma sonucuna göre ilgili agent'ı çağırır."""

    def __init__(self) -> None:
        self._classifier = RequestClassifier()

        # Lazy-init real agents
        self._medical_agent = None
        self._travel_agent = None
        self._factory_agent = None
        self._marketing_agent = None

        try:
            from agents.medical_agent import MedicalAgent
            self._medical_agent = MedicalAgent()
        except Exception as e:
            logger.warning(f"MedicalAgent init failed: {e}")

        try:
            from agents.travel_agent import TravelAgent
            self._travel_agent = TravelAgent()
        except Exception as e:
            logger.warning(f"TravelAgent init failed: {e}")

        try:
            from agents.factory_agent import FactoryAgent
            self._factory_agent = FactoryAgent()
        except Exception as e:
            logger.warning(f"FactoryAgent init failed: {e}")

        try:
            from agents.marketing_agent import MarketingAgent
            self._marketing_agent = MarketingAgent()
        except Exception as e:
            logger.warning(f"MarketingAgent init failed: {e}")

        logger.info("AgentRouter initialized — Medical | Travel | Factory | Marketing routing active.")

    def route(self, user_input: str | dict[str, Any]) -> dict[str, Any]:
        """
        Kullanıcı girdisini sınıflandırır ve uygun agent'a yönlendirir.

        Args:
            user_input: String metin veya {"message": "..."} formatında dict.

        Returns:
            Yönlendirme raporu dict olarak.
        """
        # Normalize input
        if isinstance(user_input, dict):
            text = user_input.get("message") or user_input.get("text") or json.dumps(user_input)
        else:
            text = str(user_input)

        logger.info(f"Incoming request ({len(text)} chars): {text[:120]}...")

        result = self._classifier.classify(text)

        logger.info(
            f"Classification → {result.sector.value} "
            f"(confidence={result.confidence:.2f}) | "
            f"Keywords: {result.matched_keywords[:3]}"
        )

        # Route to agent
        response = self._dispatch(result)

        # Log to AGENT_SESSION.log
        self._log_session(result, response)

        return {
            "classification": result.to_dict(),
            "agent_response": response,
        }

    def _dispatch(self, result: ClassificationResult) -> dict[str, Any]:
        """Agent'a yönlendir."""
        sector = result.sector

        if sector == Sector.MEDICAL:
            return self._call_medical_agent(result)
        elif sector == Sector.TRAVEL:
            return self._call_travel_agent(result)
        elif sector == Sector.FACTORY:
            return self._call_factory_agent(result)
        elif sector == Sector.MARKETING:
            return self._call_marketing_agent(result)
        else:
            return {
                "status": "unrouted",
                "message": (
                    "Sektör belirlenemedi. Lütfen talebinizi "
                    "'Medical', 'Travel', 'Factory' veya 'Marketing' kategorisine "
                    "girecek şekilde yeniden ifade edin."
                ),
            }

    # ------------------------------------------------------------------
    # Agent stubs — her biri agents/ klasörüne taşınacak
    # ------------------------------------------------------------------

    def _call_medical_agent(self, result: ClassificationResult) -> dict[str, Any]:
        logger.info("[MedicalAgent] Handling patient/referral request.")
        if self._medical_agent:
            try:
                return {
                    "agent": "MedicalAgent",
                    "status": "active",
                    "sector": "Medical",
                    "action": "referral_coordination",
                    "classification": result.to_dict(),
                    **self._medical_agent.process_intake({
                        "procedure_interest": result.raw_input,
                        "language": "tr",
                    }),
                }
            except Exception as e:
                logger.error(f"MedicalAgent error: {e}")
        return {
            "agent": "MedicalAgent",
            "status": "active",
            "sector": "Medical",
            "action": "referral_coordination",
            "message": (
                "Tıbbi danışmanlık talebiniz alındı. "
                "AntiGravity Phuket koordinatörünüz en geç 5 dakika içinde "
                "WhatsApp üzerinden sizinle iletişime geçecek."
            ),
            "next_steps": [
                "Ön konsültasyon rezervasyonu",
                "Medikal dosya hazırlama",
                "Türkiye partner hastane eşleştirme",
            ],
            "commission_model": "20-25% referral",
        }

    def _call_travel_agent(self, result: ClassificationResult) -> dict[str, Any]:
        logger.info("[TravelAgent] Handling hotel/restaurant/booking request.")
        if self._travel_agent:
            try:
                return {
                    "agent": "TravelAgent",
                    "status": "active",
                    "sector": "Travel",
                    "action": "booking_coordination",
                    **self._travel_agent.handle({"message": result.raw_input}),
                }
            except Exception as e:
                logger.error(f"TravelAgent error: {e}")
        return {
            "agent": "TravelAgent",
            "status": "active",
            "sector": "Travel",
            "action": "booking_coordination",
            "message": (
                "Konaklama / rezervasyon talebiniz alındı. "
                "Phuket operasyon ekibimiz müsaitlik durumunu kontrol edecek."
            ),
            "next_steps": [
                "Müsaitlik kontrolü",
                "Fiyat teklifi",
                "Rezervasyon onayı",
            ],
            "property": "Phuket Town Hotel (60 rooms)",
        }

    def _call_factory_agent(self, result: ClassificationResult) -> dict[str, Any]:
        logger.info("[FactoryAgent] Handling B2B manufacturing/textile request.")
        if self._factory_agent:
            try:
                return {
                    "agent": "FactoryAgent",
                    "status": "active",
                    "sector": "Factory",
                    "action": "b2b_lead_qualification",
                    **self._factory_agent.handle({"message": result.raw_input}),
                }
            except Exception as e:
                logger.error(f"FactoryAgent error: {e}")
        return {
            "agent": "FactoryAgent",
            "status": "dormant",
            "sector": "Factory",
            "action": "b2b_lead_qualification",
            "message": (
                "B2B / üretim talebiniz alındı. "
                "Kayıt sistemi aktif değil — bu sektör dormant modda."
            ),
            "next_steps": ["Lead kaydı", "Aktivasyon sonrası takip"],
            "note": "Factory agent currently DORMANT.",
        }

    def _call_marketing_agent(self, result: ClassificationResult) -> dict[str, Any]:
        logger.info("[MarketingAgent] Handling marketing/SEO/campaign request.")
        if self._marketing_agent:
            try:
                return {
                    "agent": "MarketingAgent",
                    "status": "active",
                    "sector": "Marketing",
                    "action": "marketing_coordination",
                    **self._marketing_agent.handle({"message": result.raw_input}),
                }
            except Exception as e:
                logger.error(f"MarketingAgent error: {e}")
        return {
            "agent": "MarketingAgent",
            "status": "active",
            "sector": "Marketing",
            "action": "marketing_coordination",
            "message": (
                "Pazarlama talebiniz alındı. "
                "SEO, içerik üretimi, kampanya planlaması ve "
                "analitik raporlama hizmetleri aktiftir."
            ),
            "capabilities": [
                "SEO keyword analizi & meta tag üretimi",
                "Blog/reklam/sosyal medya içerik üretimi",
                "Google Ads / Meta Ads / Yandex kampanya planı",
                "Performans metrikleri & ROI hesaplama",
                "Lead segmentasyonu & remarketing",
                "Otomatik platform yayınlama",
            ],
        }

    def _log_session(self, result: ClassificationResult, response: dict[str, Any]) -> None:
        """AGENT_SESSION.log'a yapılandırılmış kayıt yazar."""
        log_entry = {
            "timestamp": result.timestamp,
            "sector": result.sector.value,
            "confidence": result.confidence,
            "keywords_matched": result.matched_keywords,
            "reasoning": result.reasoning,
            "agent_dispatched": response.get("agent", "unknown"),
            "action": response.get("action", "unknown"),
        }
        logger.info(f"SESSION LOG: {json.dumps(log_entry, ensure_ascii=False)}")


# ---------------------------------------------------------------------------
# CLI Entrypoint
# ---------------------------------------------------------------------------
def main() -> None:
    """İnteraktif mod — terminal üzerinden test için."""
    router = AgentRouter()

    print("\n" + "=" * 60)
    print("  AntiGravity Ventures — Master Orchestrator v1.0.0")
    print("  Sektörler: Medical | Travel | Factory | Marketing")
    print("  Çıkmak için: Ctrl+C veya 'quit'")
    print("=" * 60 + "\n")

    while True:
        try:
            user_input = input("📨 Gelen talep: ").strip()
            if not user_input or user_input.lower() in ("quit", "exit", "q"):
                break

            output = router.route(user_input)

            print(f"\n✅ Sınıflandırma : {output['classification']['sector']}")
            print(f"   Güven         : {output['classification']['confidence']:.0%}")
            print(f"   Eşleşen KW    : {output['classification']['matched_keywords'][:5]}")
            print(f"   Agent         : {output['agent_response'].get('agent', 'N/A')}")
            print(f"   Mesaj         : {output['agent_response']['message']}\n")

        except KeyboardInterrupt:
            print("\n\nOrchestrator kapatıldı.")
            break


if __name__ == "__main__":
    main()
