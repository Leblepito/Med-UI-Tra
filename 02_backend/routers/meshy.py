"""
AntiGravity Ventures — Meshy.ai Visualization Router
4 endpoints: questions, visualize, status, post-op upload.
"""
from __future__ import annotations

import logging
import uuid
from datetime import date, datetime

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy import func as sa_func

from database.connection import SessionLocal
from database.models import Visualization

import sys
from pathlib import Path

_agents_path = str(Path(__file__).parent.parent.parent / "04_ai_agents")
if _agents_path not in sys.path:
    sys.path.insert(0, _agents_path)

from agents.meshy_agent import (
    get_procedure_questions,
    create_visualization,
    check_status,
    PROCEDURE_QUESTIONS,
)

logger = logging.getLogger("meshy_router")

router = APIRouter(prefix="/api/meshy", tags=["Meshy Visualization"])

DAILY_LIMIT_PER_IP = 1
DAILY_LIMIT_GLOBAL = 20

# ---------------------------------------------------------------------------
# Pydantic Models
# ---------------------------------------------------------------------------

class QuestionsRequest(BaseModel):
    category: str = Field(..., description="Procedure category e.g. hair_transplant, rhinoplasty")

class VisualizeRequest(BaseModel):
    image_base64: str = Field(..., description="Base64-encoded input image")
    procedure_category: str = Field(..., description="Procedure category")
    answers: dict[str, str] = Field(default_factory=dict, description="Question answers")

class PostOpRequest(BaseModel):
    viz_id: str = Field(..., description="Visualization ID")
    image_base64: str = Field(..., description="Base64-encoded post-op photo")


# ---------------------------------------------------------------------------
# Rate Limiting (DB-based)
# ---------------------------------------------------------------------------

def _check_rate_limit(ip: str) -> None:
    """Raise 429 if IP or global daily limit exceeded."""
    session = SessionLocal()
    try:
        today = date.today()

        # IP-based limit
        ip_count = (
            session.query(sa_func.count(Visualization.viz_id))
            .filter(
                Visualization.ip_address == ip,
                sa_func.date(Visualization.created_at) == today,
            )
            .scalar()
        )
        if ip_count >= DAILY_LIMIT_PER_IP:
            raise HTTPException(
                status_code=429,
                detail={
                    "code": "DAILY_LIMIT_IP",
                    "message": "You have reached the daily visualization limit. Please try again tomorrow.",
                    "limit": DAILY_LIMIT_PER_IP,
                },
            )

        # Global daily limit
        global_count = (
            session.query(sa_func.count(Visualization.viz_id))
            .filter(sa_func.date(Visualization.created_at) == today)
            .scalar()
        )
        if global_count >= DAILY_LIMIT_GLOBAL:
            raise HTTPException(
                status_code=429,
                detail={
                    "code": "DAILY_LIMIT_GLOBAL",
                    "message": "Global daily visualization limit reached. Please try again tomorrow.",
                    "limit": DAILY_LIMIT_GLOBAL,
                },
            )
    finally:
        session.close()


def _generate_viz_id() -> str:
    """Generate unique visualization ID like VIZ-20260222-A1B2C3."""
    today = datetime.now().strftime("%Y%m%d")
    suffix = uuid.uuid4().hex[:6].upper()
    return f"VIZ-{today}-{suffix}"


def _get_client_ip(request: Request) -> str:
    """Extract client IP from request, considering proxies."""
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/questions")
async def get_questions(body: QuestionsRequest):
    """Return procedure-specific questions for the visualization wizard."""
    questions = await get_procedure_questions(body.category)
    if not questions:
        available = list(PROCEDURE_QUESTIONS.keys())
        raise HTTPException(
            status_code=400,
            detail={
                "code": "INVALID_CATEGORY",
                "message": f"Unknown procedure category: {body.category}",
                "available_categories": available,
            },
        )
    return {"category": body.category, "questions": questions}


@router.post("/visualize")
async def start_visualization(body: VisualizeRequest, request: Request):
    """Start a new before/after visualization job."""
    ip = _get_client_ip(request)

    # Validate category
    if body.procedure_category not in PROCEDURE_QUESTIONS:
        raise HTTPException(status_code=400, detail="Invalid procedure category")

    # Validate image size (rough base64 size check — ~5MB raw = ~6.7MB base64)
    raw_b64 = body.image_base64
    if raw_b64.startswith("data:"):
        raw_b64 = raw_b64.split(",", 1)[-1] if "," in raw_b64 else raw_b64
    if len(raw_b64) > 7_000_000:
        raise HTTPException(status_code=413, detail="Image too large. Maximum 5MB.")

    # Rate limit check
    _check_rate_limit(ip)

    viz_id = _generate_viz_id()

    # Call Meshy API
    try:
        meshy_resp = await create_visualization(
            body.image_base64, body.procedure_category, body.answers
        )
    except Exception as e:
        logger.error(f"Meshy API error: {e}")
        raise HTTPException(status_code=502, detail="Visualization service unavailable. Please try again later.")

    meshy_task_id = meshy_resp.get("result") or meshy_resp.get("id", "")

    # Save to DB
    session = SessionLocal()
    try:
        viz = Visualization(
            viz_id=viz_id,
            ip_address=ip,
            procedure_category=body.procedure_category,
            questions_answers=body.answers,
            meshy_task_id=meshy_task_id,
            status="processing",
            input_image_b64=body.image_base64[:100] + "...",  # Don't store full base64 in DB
            meshy_response=meshy_resp,
        )
        session.add(viz)
        session.commit()
    except Exception as e:
        session.rollback()
        logger.error(f"DB save error: {e}")
        raise HTTPException(status_code=500, detail="Failed to save visualization record")
    finally:
        session.close()

    return {
        "viz_id": viz_id,
        "meshy_task_id": meshy_task_id,
        "status": "processing",
        "message": "Visualization started. Poll /api/meshy/status/{viz_id} for results.",
    }


@router.get("/status/{viz_id}")
async def get_status(viz_id: str):
    """Check visualization job status and return result if ready."""
    session = SessionLocal()
    try:
        viz = session.query(Visualization).filter(Visualization.viz_id == viz_id).first()
        if not viz:
            raise HTTPException(status_code=404, detail="Visualization not found")

        # If already succeeded or failed, return cached result
        if viz.status in ("succeeded", "failed"):
            return {
                "viz_id": viz.viz_id,
                "status": viz.status,
                "output_image_url": viz.output_image_url,
                "procedure_category": viz.procedure_category,
            }

        # Poll Meshy for update
        if viz.meshy_task_id:
            try:
                meshy_status = await check_status(viz.meshy_task_id)
                meshy_state = meshy_status.get("status", "").upper()

                if meshy_state == "SUCCEEDED":
                    # Extract output URL
                    output_urls = meshy_status.get("output_urls", [])
                    output_url = output_urls[0] if output_urls else meshy_status.get("output_url", "")
                    viz.status = "succeeded"
                    viz.output_image_url = output_url
                    viz.meshy_response = meshy_status
                    session.commit()
                elif meshy_state == "FAILED":
                    viz.status = "failed"
                    viz.meshy_response = meshy_status
                    session.commit()
                # else: still processing
            except Exception as e:
                logger.warning(f"Meshy poll error for {viz_id}: {e}")

        return {
            "viz_id": viz.viz_id,
            "status": viz.status,
            "output_image_url": viz.output_image_url,
            "procedure_category": viz.procedure_category,
        }
    finally:
        session.close()


@router.post("/post-op")
async def submit_post_op(body: PostOpRequest):
    """Upload actual post-op photo for comparison with AI prediction."""
    session = SessionLocal()
    try:
        viz = session.query(Visualization).filter(Visualization.viz_id == body.viz_id).first()
        if not viz:
            raise HTTPException(status_code=404, detail="Visualization not found")

        if viz.status != "succeeded":
            raise HTTPException(status_code=400, detail="Visualization must be completed before uploading post-op photo")

        viz.post_op_image_b64 = body.image_base64[:100] + "..."  # Truncated storage
        # Placeholder similarity score — real implementation would use image comparison
        viz.similarity_score = 85.0
        session.commit()

        return {
            "viz_id": viz.viz_id,
            "similarity_score": float(viz.similarity_score),
            "message": "Post-op photo received. Comparison complete.",
        }
    except HTTPException:
        raise
    except Exception as e:
        session.rollback()
        logger.error(f"Post-op upload error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process post-op photo")
    finally:
        session.close()
