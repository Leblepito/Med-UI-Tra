"""
AntiGravity Ventures — Factory Agent
B2B tekstil ve üretim talebi yönetimi (şu an dormant).
"""
from __future__ import annotations

import logging

logger = logging.getLogger("FactoryAgent")

ACTIVATION_CRITERIA = {
    "tourism_profitable_months": {"required": 6, "current": 0},
    "trading_profitable_months": {"required": 3, "current": 0},
    "lead_pipeline_ready": {"required": True, "current": False},
}


class FactoryAgent:
    """
    Sorumluluklar (Dormant — Phase 4+):
    - B2B tekstil ve konfeksiyon talep yönetimi
    - Türkiye fabrika eşleştirme
    - Numune / sipariş akışı
    - İhracat/ithalat belge desteği
    """

    STATUS = "DORMANT"

    def handle(self, request: dict) -> dict:
        logger.warning(f"FactoryAgent is DORMANT. Request queued: {request}")
        return {
            "status": "queued",
            "agent": "FactoryAgent",
            "dormant": True,
            "activation_criteria": ACTIVATION_CRITERIA,
            "message": (
                "B2B/Fabrika sektörü henüz aktif değil. "
                "Talebiniz kayıt altına alındı. "
                "Aktivasyon koşulları sağlandığında sisteminize dönüş yapılacak."
            ),
            "estimated_activation": "Phase 4 (Month 7+)",
        }

    @classmethod
    def activation_ready(cls) -> bool:
        return all(
            (c["current"] >= c["required"])
            if isinstance(c["required"], (int, float))
            else (c["current"] == c["required"])
            for c in ACTIVATION_CRITERIA.values()
        )
