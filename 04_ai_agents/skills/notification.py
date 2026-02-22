"""
AntiGravity Ventures — Unified Notification Service
WhatsApp Business API + Telegram Bot API + LINE Messaging API.

Region-aware channel selection:
  - Turkey / Europe / UAE → WhatsApp
  - Russia / CIS → Telegram
  - Thailand / Asia → LINE
"""
from __future__ import annotations

import logging
import os
from typing import Optional

import httpx

logger = logging.getLogger("NotificationService")

# ---------------------------------------------------------------------------
# Region → Channel mapping
# ---------------------------------------------------------------------------

REGION_CHANNEL_MAP: dict[str, str] = {
    "turkey": "whatsapp",
    "europe": "whatsapp",
    "uae": "whatsapp",
    "middle_east": "whatsapp",
    "russia": "telegram",
    "cis": "telegram",
    "thailand": "line",
    "asia": "line",
    "japan": "line",
}

LANGUAGE_REGION_MAP: dict[str, str] = {
    "tr": "turkey",
    "en": "europe",
    "ru": "russia",
    "th": "thailand",
    "ar": "uae",
    "zh": "asia",
}


class NotificationService:
    """Unified notification sender for WhatsApp, Telegram, and LINE."""

    def __init__(self) -> None:
        # WhatsApp Business Cloud API
        self.whatsapp_token = os.getenv("WHATSAPP_TOKEN", "")
        self.whatsapp_phone_id = os.getenv("WHATSAPP_PHONE_ID", "")

        # Telegram Bot API
        self.telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.telegram_coordinator_chat_id = os.getenv("TELEGRAM_COORDINATOR_CHAT_ID", "")

        # LINE Messaging API
        self.line_channel_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
        self.line_channel_secret = os.getenv("LINE_CHANNEL_SECRET", "")

    # ------------------------------------------------------------------
    # Channel availability
    # ------------------------------------------------------------------

    def get_active_channels(self) -> list[dict]:
        """Return list of configured notification channels."""
        channels = []
        if self.whatsapp_token and self.whatsapp_phone_id:
            channels.append({"channel": "whatsapp", "status": "active", "regions": ["Turkey", "Europe", "UAE"]})
        else:
            channels.append({"channel": "whatsapp", "status": "not_configured", "regions": ["Turkey", "Europe", "UAE"]})

        if self.telegram_bot_token:
            channels.append({"channel": "telegram", "status": "active", "regions": ["Russia", "CIS"]})
        else:
            channels.append({"channel": "telegram", "status": "not_configured", "regions": ["Russia", "CIS"]})

        if self.line_channel_token:
            channels.append({"channel": "line", "status": "active", "regions": ["Thailand", "Asia"]})
        else:
            channels.append({"channel": "line", "status": "not_configured", "regions": ["Thailand", "Asia"]})

        return channels

    # ------------------------------------------------------------------
    # WhatsApp Business Cloud API
    # ------------------------------------------------------------------

    async def send_whatsapp(self, phone: str, message: str, language: str = "en") -> dict:
        """Send a WhatsApp text message via Business Cloud API."""
        if not self.whatsapp_token or not self.whatsapp_phone_id:
            logger.warning("WhatsApp not configured — skipping")
            return {"sent": False, "channel": "whatsapp", "reason": "not_configured"}

        url = f"https://graph.facebook.com/v18.0/{self.whatsapp_phone_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.whatsapp_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": phone.replace("+", "").replace(" ", ""),
            "type": "text",
            "text": {"body": message},
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(url, json=payload, headers=headers)
                if resp.status_code == 200:
                    logger.info(f"WhatsApp sent to {phone[:6]}***")
                    return {"sent": True, "channel": "whatsapp", "status_code": resp.status_code}
                else:
                    logger.error(f"WhatsApp API error: {resp.status_code} — {resp.text}")
                    return {"sent": False, "channel": "whatsapp", "status_code": resp.status_code, "error": resp.text}
        except Exception as e:
            logger.error(f"WhatsApp send failed: {e}")
            return {"sent": False, "channel": "whatsapp", "error": str(e)}

    # ------------------------------------------------------------------
    # Telegram Bot API
    # ------------------------------------------------------------------

    async def send_telegram(self, chat_id: str, message: str) -> dict:
        """Send a Telegram message via Bot API."""
        if not self.telegram_bot_token:
            logger.warning("Telegram not configured — skipping")
            return {"sent": False, "channel": "telegram", "reason": "not_configured"}

        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML",
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(url, json=payload)
                if resp.status_code == 200:
                    logger.info(f"Telegram sent to chat {chat_id}")
                    return {"sent": True, "channel": "telegram", "status_code": resp.status_code}
                else:
                    logger.error(f"Telegram API error: {resp.status_code} — {resp.text}")
                    return {"sent": False, "channel": "telegram", "status_code": resp.status_code, "error": resp.text}
        except Exception as e:
            logger.error(f"Telegram send failed: {e}")
            return {"sent": False, "channel": "telegram", "error": str(e)}

    # ------------------------------------------------------------------
    # LINE Messaging API
    # ------------------------------------------------------------------

    async def send_line(self, user_id: str, message: str) -> dict:
        """Send a LINE push message."""
        if not self.line_channel_token:
            logger.warning("LINE not configured — skipping")
            return {"sent": False, "channel": "line", "reason": "not_configured"}

        url = "https://api.line.me/v2/bot/message/push"
        headers = {
            "Authorization": f"Bearer {self.line_channel_token}",
            "Content-Type": "application/json",
        }
        payload = {
            "to": user_id,
            "messages": [{"type": "text", "text": message}],
        }

        try:
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.post(url, json=payload, headers=headers)
                if resp.status_code == 200:
                    logger.info(f"LINE sent to {user_id[:8]}***")
                    return {"sent": True, "channel": "line", "status_code": resp.status_code}
                else:
                    logger.error(f"LINE API error: {resp.status_code} — {resp.text}")
                    return {"sent": False, "channel": "line", "status_code": resp.status_code, "error": resp.text}
        except Exception as e:
            logger.error(f"LINE send failed: {e}")
            return {"sent": False, "channel": "line", "error": str(e)}

    # ------------------------------------------------------------------
    # High-level: Coordinator notification
    # ------------------------------------------------------------------

    async def notify_coordinator(self, patient_data: dict) -> dict:
        """
        Send coordinator notification based on patient region/language.
        Always sends to Telegram coordinator chat as backup.
        """
        language = patient_data.get("language", "en")
        region = LANGUAGE_REGION_MAP.get(language, "europe")
        channel = REGION_CHANNEL_MAP.get(region, "whatsapp")

        patient_id = patient_data.get("patient_id", "N/A")
        full_name = patient_data.get("full_name", "N/A")
        procedure = patient_data.get("procedure_interest", "N/A")
        phone = patient_data.get("phone", "N/A")

        message = (
            f"New Patient Intake\n"
            f"ID: {patient_id}\n"
            f"Name: {full_name}\n"
            f"Procedure: {procedure}\n"
            f"Phone: {phone}\n"
            f"Language: {language}\n"
            f"Region: {region}\n"
            f"Channel: {channel}"
        )

        results = {}

        # Always notify coordinator via Telegram
        if self.telegram_coordinator_chat_id:
            results["telegram"] = await self.send_telegram(self.telegram_coordinator_chat_id, message)

        # Also send via region-preferred channel if different
        if channel == "whatsapp" and self.whatsapp_token:
            coordinator_phone = os.getenv("COORDINATOR_WHATSAPP", "")
            if coordinator_phone:
                results["whatsapp"] = await self.send_whatsapp(coordinator_phone, message)
        elif channel == "line" and self.line_channel_token:
            coordinator_line = os.getenv("COORDINATOR_LINE_ID", "")
            if coordinator_line:
                results["line"] = await self.send_line(coordinator_line, message)

        return {"patient_id": patient_id, "region": region, "channel": channel, "results": results}

    # ------------------------------------------------------------------
    # High-level: Patient notification
    # ------------------------------------------------------------------

    async def notify_patient(
        self,
        phone: str,
        message: str,
        preferred_channel: Optional[str] = None,
        language: str = "en",
    ) -> dict:
        """Send notification to patient on their preferred channel."""
        if not preferred_channel:
            region = LANGUAGE_REGION_MAP.get(language, "europe")
            preferred_channel = REGION_CHANNEL_MAP.get(region, "whatsapp")

        if preferred_channel == "whatsapp":
            return await self.send_whatsapp(phone, message, language)
        elif preferred_channel == "telegram":
            return await self.send_telegram(phone, message)
        elif preferred_channel == "line":
            return await self.send_line(phone, message)
        else:
            return {"sent": False, "channel": preferred_channel, "reason": "unknown_channel"}
