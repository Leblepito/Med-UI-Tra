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

    def process_request(self, request: dict) -> dict:
        """
        Travel router tarafından çağrılan ana metod.
        Coordinator mesajı ve öneri listesi döndürür.
        """
        lang = request.get("language", "en")
        destination = request.get("destination", "Phuket")
        check_in = request.get("check_in") or ""
        guests = request.get("guests", 2)
        request_id = request.get("request_id", "TRV-UNKNOWN")

        coord_msgs = {
            "ru": f"Здравствуйте! 🏖️\n\nВаш запрос #{request_id} получен.\nКоординатор свяжется с вами через WhatsApp в течение 5 минут.\n\n📍 Направление: {destination}\n👥 Гостей: {guests}",
            "en": f"Hello! 🏖️\n\nYour request #{request_id} has been received.\nOur coordinator will contact you via WhatsApp within 5 minutes.\n\n📍 Destination: {destination}\n👥 Guests: {guests}",
            "tr": f"Merhaba! 🏖️\n\n#{request_id} numaralı talebiniz alındı.\nKoordinatörümüz 5 dakika içinde WhatsApp'tan iletişime geçecek.\n\n📍 Destinasyon: {destination}\n👥 Misafir: {guests}",
        }

        suggestions = [
            {"name": "Patong Beach Hotel", "stars": 4, "price_night_usd": 85, "highlight": "Beach front"},
            {"name": "Kamala Bay Suites", "stars": 5, "price_night_usd": 150, "highlight": "Private pool"},
            {"name": "Kata Garden Resort", "stars": 3, "price_night_usd": 60, "highlight": "Family friendly"},
        ]

        logger.info(f"[TravelAgent] Travel request processed: {request_id} → {destination}")

        return {
            "request_id": request_id,
            "coordinator_message": coord_msgs.get(lang, coord_msgs["en"]),
            "suggestions": suggestions,
        }

