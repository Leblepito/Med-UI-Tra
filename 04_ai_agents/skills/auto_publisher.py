"""
AntiGravity Ventures — Marketing: Auto Publisher
Platform-specific formatlama, zamanlama ve yayinlama yonetimi.
"""
from __future__ import annotations

import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

# Backend path for DB imports
_backend_path = str(Path(__file__).parent.parent.parent / "02_backend")
if _backend_path not in sys.path:
    sys.path.insert(0, _backend_path)

try:
    from database.models import PublishQueueItem
    _DB_AVAILABLE = True
except ImportError:
    _DB_AVAILABLE = False


# ---------------------------------------------------------------------------
# Publish queue (in-memory fallback when db=None)
# ---------------------------------------------------------------------------
_publish_queue: list[dict[str, Any]] = []

# Optimal yayin saatleri (UTC, bolge/platform bazli)
BEST_PUBLISH_TIMES: dict[str, dict[str, str]] = {
    "google": {
        "turkey": "09:00", "russia": "10:00", "uae": "08:00",
        "europe": "10:00", "asia": "11:00",
    },
    "meta": {
        "turkey": "12:00", "russia": "13:00", "uae": "11:00",
        "europe": "12:00", "asia": "12:00",
    },
    "instagram": {
        "turkey": "19:00", "russia": "20:00", "uae": "18:00",
        "europe": "18:00", "asia": "19:00",
    },
    "yandex": {
        "russia": "10:00", "turkey": "09:00",
    },
    "vk": {
        "russia": "20:00",
    },
    "line": {
        "asia": "12:00",
    },
}

# Platform-specific format kuralari
PLATFORM_FORMATS: dict[str, dict[str, Any]] = {
    "google": {
        "name": "Google Ads",
        "max_headline": 30,
        "max_description": 90,
        "formats": ["responsive_search", "display", "video"],
        "requirements": "Headlines (max 15x30 chars), Descriptions (max 4x90 chars)",
    },
    "meta": {
        "name": "Meta Ads (Facebook/Instagram)",
        "max_primary_text": 125,
        "max_headline": 40,
        "formats": ["image", "video", "carousel", "stories"],
        "requirements": "Primary text (125 chars), Headline (40 chars), Image ratio 1:1 or 9:16",
    },
    "yandex": {
        "name": "Yandex Direct",
        "max_title": 56,
        "max_text": 81,
        "formats": ["text", "image", "video"],
        "requirements": "Title (56 chars), Text (81 chars), Sitelinks (max 4)",
    },
    "vk": {
        "name": "VK Ads",
        "max_title": 33,
        "max_description": 70,
        "formats": ["post", "carousel", "stories"],
        "requirements": "Title (33 chars), Description (70 chars)",
    },
    "instagram": {
        "name": "Instagram",
        "max_caption": 2200,
        "max_hashtags": 30,
        "formats": ["post", "stories", "reels", "carousel"],
        "requirements": "Caption (2200 chars), Hashtags (max 30), Image ratio varies",
    },
    "line": {
        "name": "LINE",
        "max_message": 500,
        "formats": ["text", "rich_message", "card"],
        "requirements": "Message (500 chars), Rich content supported",
    },
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def format_for_platform(content: str, platform: str) -> dict[str, Any]:
    """Icerigi platform-specific formata donusturur."""
    plat = platform.lower()
    fmt = PLATFORM_FORMATS.get(plat, {})

    if plat == "google":
        lines = content.split("\n")
        headline = (lines[0] if lines else content)[:fmt.get("max_headline", 30)]
        description = content[:fmt.get("max_description", 90)]
        formatted = {"headline": headline, "description": description}
    elif plat == "meta":
        formatted = {
            "primary_text": content[:fmt.get("max_primary_text", 125)],
            "headline": content.split("\n")[0][:fmt.get("max_headline", 40)] if content else "",
        }
    elif plat == "yandex":
        formatted = {
            "title": content.split("\n")[0][:fmt.get("max_title", 56)] if content else "",
            "text": content[:fmt.get("max_text", 81)],
        }
    elif plat == "vk":
        formatted = {
            "title": content.split("\n")[0][:fmt.get("max_title", 33)] if content else "",
            "description": content[:fmt.get("max_description", 70)],
        }
    elif plat == "instagram":
        formatted = {
            "caption": content[:fmt.get("max_caption", 2200)],
            "hashtag_count": content.count("#"),
        }
    elif plat == "line":
        formatted = {"message": content[:fmt.get("max_message", 500)]}
    else:
        formatted = {"text": content}

    return {
        "platform": plat,
        "platform_name": fmt.get("name", platform.title()),
        "formatted_content": formatted,
        "requirements": fmt.get("requirements", ""),
        "available_formats": fmt.get("formats", []),
    }


def schedule_post(content: str, platform: str, publish_at: str, db=None) -> dict[str, Any]:
    """Icerik yayinini zamanlar."""
    post_id = f"PUB-{uuid.uuid4().hex[:8].upper()}"

    if db and _DB_AVAILABLE:
        item = PublishQueueItem(
            post_id=post_id,
            content=content,
            platform=platform,
            publish_at=publish_at if publish_at else None,
            status="scheduled",
        )
        db.add(item)
        db.commit()
        queue_pos = db.query(PublishQueueItem).count()
    else:
        entry = {
            "post_id": post_id,
            "content": content,
            "platform": platform,
            "publish_at": publish_at,
            "status": "scheduled",
            "created_at": datetime.utcnow().isoformat(),
        }
        _publish_queue.append(entry)
        queue_pos = len(_publish_queue)

    return {
        "post_id": post_id,
        "status": "scheduled",
        "platform": platform,
        "publish_at": publish_at,
        "queue_position": queue_pos,
    }


def publish(content: str, platform: str, credentials: dict | None = None, db=None) -> dict[str, Any]:
    """Icerigi hemen yayinlar (stub — gercek API entegrasyonu Phase 2)."""
    post_id = f"PUB-{uuid.uuid4().hex[:8].upper()}"
    now = datetime.utcnow()

    if db and _DB_AVAILABLE:
        item = PublishQueueItem(
            post_id=post_id,
            content=content,
            platform=platform,
            status="published_stub",
            published_at=now,
        )
        db.add(item)
        db.commit()
    else:
        entry = {
            "post_id": post_id,
            "content": content,
            "platform": platform,
            "status": "published_stub",
            "published_at": now.isoformat(),
        }
        _publish_queue.append(entry)

    return {
        "post_id": post_id,
        "status": "published_stub",
        "platform": platform,
        "published_at": now.isoformat(),
        "note": f"Stub publish — real {platform} API integration planned for Phase 2",
    }


def get_publish_queue(db=None) -> dict[str, Any]:
    """Bekleyen ve tamamlanan yayinlar listesi."""
    if db and _DB_AVAILABLE:
        all_items = db.query(PublishQueueItem).all()
        all_dicts = [item.to_dict() for item in all_items]
        scheduled = [p for p in all_dicts if p["status"] == "scheduled"]
        published = [p for p in all_dicts if "published" in p["status"]]
        return {
            "total": len(all_dicts),
            "scheduled": {"count": len(scheduled), "posts": scheduled},
            "published": {"count": len(published), "posts": published},
        }

    scheduled = [p for p in _publish_queue if p["status"] == "scheduled"]
    published = [p for p in _publish_queue if "published" in p["status"]]

    return {
        "total": len(_publish_queue),
        "scheduled": {"count": len(scheduled), "posts": scheduled},
        "published": {"count": len(published), "posts": published},
    }


def get_best_publish_time(platform: str, region: str, lang: str | None = None) -> dict[str, Any]:
    """Optimal yayin saati onerir."""
    plat = platform.lower()
    reg = region.lower()

    time_utc = BEST_PUBLISH_TIMES.get(plat, {}).get(reg, "12:00")

    # Timezone offset hints
    tz_offsets = {
        "turkey": "+03:00",
        "russia": "+03:00",
        "uae": "+04:00",
        "europe": "+01:00",
        "asia": "+07:00",
    }

    offset = tz_offsets.get(reg, "+00:00")

    return {
        "platform": plat,
        "region": reg,
        "recommended_time_utc": time_utc,
        "timezone_offset": offset,
        "reasoning": f"Peak engagement for {plat} in {reg} is around {time_utc} UTC ({offset})",
    }


def get_supported_platforms() -> dict[str, Any]:
    """Desteklenen platformlarin listesi ve format kurallarini dondurur."""
    return {
        "platforms": {
            k: {
                "name": v["name"],
                "requirements": v.get("requirements", ""),
                "formats": v.get("formats", []),
            }
            for k, v in PLATFORM_FORMATS.items()
        },
        "total": len(PLATFORM_FORMATS),
    }
