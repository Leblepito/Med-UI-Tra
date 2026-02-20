"""
AntiGravity Ventures — Travel Agent
Phuket otel, restoran ve turizm rezervasyon koordinasyonu.
"""
from __future__ import annotations

import logging
from datetime import datetime, timedelta

logger = logging.getLogger("TravelAgent")


class TravelAgent:
    """
    Sorumluluklar:
    - Otel odası müsaitlik ve rezervasyon
    - Restoran masa rezervasyonu
    - Dinamik fiyatlandırma (sezonluk)
    - OTA kanalları (Booking.com, Airbnb) senkronizasyon
    - Rusça/İngilizce misafir iletişimi
    """

    ROOM_TYPES = {
        "standard": {"capacity": 2, "base_price_usd": 85},
        "deluxe": {"capacity": 2, "base_price_usd": 120},
        "suite": {"capacity": 4, "base_price_usd": 180},
        "family": {"capacity": 5, "base_price_usd": 160},
    }

    HIGH_SEASON_MONTHS = [11, 12, 1, 2, 3]   # Nov–Mar Phuket high season

    def handle(self, request: dict) -> dict:
        logger.info(f"TravelAgent processing: {request}")
        check_in = request.get("check_in") or datetime.utcnow().strftime("%Y-%m-%d")
        nights = int(request.get("nights", 3))
        room_type = request.get("room_type", "standard").lower()
        guests = int(request.get("guests", 2))

        price = self._calculate_price(check_in, nights, room_type)
        availability = self._check_availability(check_in, nights, room_type)

        return {
            "status": "quote_ready" if availability else "unavailable",
            "property": "AntiGravity Phuket Town Hotel",
            "room_type": room_type,
            "check_in": check_in,
            "nights": nights,
            "guests": guests,
            "price_usd": price,
            "available": availability,
            "next_action": "confirm_reservation" if availability else "suggest_alternatives",
        }

    def _calculate_price(self, check_in_str: str, nights: int, room_type: str) -> float:
        try:
            ci = datetime.strptime(check_in_str, "%Y-%m-%d")
        except ValueError:
            ci = datetime.utcnow()
        base = self.ROOM_TYPES.get(room_type, self.ROOM_TYPES["standard"])["base_price_usd"]
        multiplier = 1.35 if ci.month in self.HIGH_SEASON_MONTHS else 1.0
        return round(base * nights * multiplier, 2)

    def _check_availability(self, check_in: str, nights: int, room_type: str) -> bool:
        # Stub — gerçekte Firestore/PMS'den kontrol edilecek
        return True
