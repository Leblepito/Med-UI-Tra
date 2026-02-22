"""
AntiGravity Ventures — Notification Router
/api/notifications/* endpoints: send, test, channels, webhooks.
"""
from __future__ import annotations

import hashlib
import hmac
import logging
import os
import sys
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional

from auth import require_admin

# Ensure skills are importable
_skills_path = Path(__file__).parent.parent.parent / "04_ai_agents" / "skills"
if str(_skills_path) not in sys.path:
    sys.path.insert(0, str(_skills_path))

from notification import NotificationService  # noqa: E402

logger = logging.getLogger("thaiturk.notifications")
router = APIRouter(prefix="/api/notifications", tags=["Notifications"])
notifier = NotificationService()


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class SendNotificationRequest(BaseModel):
    channel: str = Field(..., pattern=r"^(whatsapp|telegram|line)$")
    recipient: str = Field(..., min_length=1, description="Phone number, chat_id, or LINE user_id")
    message: str = Field(..., min_length=1, max_length=4096)
    language: str = "en"


class TestNotificationRequest(BaseModel):
    channel: Optional[str] = Field(None, pattern=r"^(whatsapp|telegram|line)$")
    recipient: Optional[str] = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/channels")
def list_channels() -> dict:
    """List all notification channels and their configuration status."""
    return {"channels": notifier.get_active_channels()}


@router.post("/send")
async def send_notification(body: SendNotificationRequest, _admin=Depends(require_admin)) -> dict:
    """Send a manual notification (admin-only)."""
    if body.channel == "whatsapp":
        result = await notifier.send_whatsapp(body.recipient, body.message, body.language)
    elif body.channel == "telegram":
        result = await notifier.send_telegram(body.recipient, body.message)
    elif body.channel == "line":
        result = await notifier.send_line(body.recipient, body.message)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown channel: {body.channel}")
    return result


@router.post("/test")
async def test_notification(body: TestNotificationRequest, _admin=Depends(require_admin)) -> dict:
    """Send a test notification to verify channel configuration (admin-only)."""
    test_message = "AntiGravity ThaiTurk — Test notification. If you see this, the channel is working."
    results = {}

    channels_to_test = [body.channel] if body.channel else ["whatsapp", "telegram", "line"]

    for ch in channels_to_test:
        if ch == "whatsapp":
            recipient = body.recipient or os.getenv("COORDINATOR_WHATSAPP", "")
            if recipient:
                results["whatsapp"] = await notifier.send_whatsapp(recipient, test_message)
            else:
                results["whatsapp"] = {"sent": False, "reason": "no_recipient"}

        elif ch == "telegram":
            recipient = body.recipient or os.getenv("TELEGRAM_COORDINATOR_CHAT_ID", "")
            if recipient:
                results["telegram"] = await notifier.send_telegram(recipient, test_message)
            else:
                results["telegram"] = {"sent": False, "reason": "no_recipient"}

        elif ch == "line":
            recipient = body.recipient or os.getenv("COORDINATOR_LINE_ID", "")
            if recipient:
                results["line"] = await notifier.send_line(recipient, test_message)
            else:
                results["line"] = {"sent": False, "reason": "no_recipient"}

    return {"test_results": results}


# ---------------------------------------------------------------------------
# Incoming Webhooks
# ---------------------------------------------------------------------------

@router.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request) -> dict:
    """WhatsApp incoming message webhook."""
    body = await request.json()
    logger.info(f"WhatsApp webhook received: {body.get('entry', [{}])[0].get('id', 'unknown')}")
    # Process incoming WhatsApp messages (future: auto-reply, routing)
    return {"status": "received"}


@router.post("/webhook/telegram")
async def telegram_webhook(request: Request) -> dict:
    """Telegram incoming update webhook."""
    body = await request.json()
    logger.info(f"Telegram webhook received: update_id={body.get('update_id', 'unknown')}")
    # Process incoming Telegram messages (future: bot commands, routing)
    return {"status": "received"}


@router.post("/webhook/line")
async def line_webhook(request: Request) -> dict:
    """LINE incoming event webhook with signature verification."""
    body_bytes = await request.body()
    signature = request.headers.get("X-Line-Signature", "")
    channel_secret = os.getenv("LINE_CHANNEL_SECRET", "")

    if channel_secret and signature:
        expected = hmac.HMAC(
            channel_secret.encode("utf-8"),
            body_bytes,
            hashlib.sha256,
        ).hexdigest()
        if not hmac.compare_digest(signature, expected):
            raise HTTPException(status_code=403, detail="Invalid LINE signature")

    import json
    body = json.loads(body_bytes)
    events = body.get("events", [])
    logger.info(f"LINE webhook received: {len(events)} event(s)")
    # Process incoming LINE events (future: auto-reply, routing)
    return {"status": "received"}
