"""
AntiGravity Ventures — Marketing Sector: FastAPI Router
/api/marketing/* endpoints

SEO, icerik uretimi, kampanya planlama, analitik, lead funnel ve otomatik yayinlama.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.connection import get_db

# Agent path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "04_ai_agents"))
from agents.marketing_agent import MarketingAgent  # noqa: E402

# Pydantic models
sys.path.insert(0, str(Path(__file__).parent.parent))
from models.marketing import (  # noqa: E402
    SEOAnalyzeRequest,
    MetaTagRequest,
    ContentRequest,
    CampaignPlanRequest,
    BudgetSplitRequest,
    ROIEstimateRequest,
    AnalyticsReportRequest,
    LeadSegmentRequest,
    LeadScoreRequest,
    PublishRequest,
)

router = APIRouter(prefix="/api/marketing", tags=["Marketing"])
agent = MarketingAgent()


# ---------------------------------------------------------------------------
# SEO Endpoints
# ---------------------------------------------------------------------------

@router.post("/seo/analyze")
def seo_analyze(body: SEOAnalyzeRequest) -> dict:
    """Keyword analizi + SEO skoru."""
    return agent.generate_seo_package({
        "procedure": body.procedure,
        "region": body.region.value,
        "lang": body.lang,
    })


@router.post("/seo/meta")
def seo_meta(body: MetaTagRequest) -> dict:
    """Meta tag uretimi."""
    return agent.handle({
        "action": "seo_meta",
        "title": body.title,
        "description": body.description,
        "keywords": body.keywords,
        "lang": body.lang,
    })


# ---------------------------------------------------------------------------
# Content Endpoints
# ---------------------------------------------------------------------------

@router.post("/content/blog")
def content_blog(body: ContentRequest) -> dict:
    """Blog yazisi uretimi."""
    return agent.handle({
        "action": "content_blog",
        "procedure": body.procedure,
        "region": body.region.value,
        "lang": body.lang,
        "tone": body.tone,
    })


@router.post("/content/ad-copy")
def content_ad_copy(body: ContentRequest) -> dict:
    """Reklam metni uretimi."""
    return agent.handle({
        "action": "content_ad",
        "procedure": body.procedure,
        "platform": body.platform.value if body.platform else "google",
        "region": body.region.value,
        "lang": body.lang,
    })


@router.post("/content/social")
def content_social(body: ContentRequest) -> dict:
    """Sosyal medya postu uretimi."""
    return agent.handle({
        "action": "content_social",
        "procedure": body.procedure,
        "platform": body.platform.value if body.platform else "instagram",
        "region": body.region.value,
        "lang": body.lang,
    })


# ---------------------------------------------------------------------------
# Campaign Endpoints
# ---------------------------------------------------------------------------

@router.post("/campaign/plan")
def campaign_plan(body: CampaignPlanRequest, db: Session = Depends(get_db)) -> dict:
    """Kampanya plani olusturma."""
    from database.models import Campaign
    import uuid

    result = agent.plan_campaign({
        "procedure": body.procedure,
        "regions": [r.value for r in body.regions],
        "budget_usd": body.budget_usd,
        "duration_days": body.duration_days,
        "platforms": [p.value for p in body.platforms],
    })

    # Persist campaign to DB
    campaign_id = f"CMP-{uuid.uuid4().hex[:8].upper()}"
    campaign = Campaign(
        campaign_id=campaign_id,
        procedure=body.procedure,
        regions=[r.value for r in body.regions],
        platforms=[p.value for p in body.platforms],
        total_budget_usd=body.budget_usd,
        duration_days=body.duration_days,
        budget_split=result.get("budget_split"),
        ad_groups=result.get("ad_groups"),
        estimated_roi=result.get("estimated_roi"),
        calendar_summary=result.get("calendar_summary"),
    )
    db.add(campaign)
    db.commit()

    result["campaign_id"] = campaign_id
    return result


@router.post("/campaign/budget")
def campaign_budget(body: BudgetSplitRequest) -> dict:
    """Butce dagilimi hesaplama."""
    return agent.handle({
        "action": "campaign_budget",
        "total_budget": body.total_budget,
        "regions": [r.value for r in body.regions],
        "platforms": [p.value for p in body.platforms],
    })


@router.get("/campaign/roi")
def campaign_roi(
    procedure: str = "hair_transplant",
    budget_usd: float = 1000,
    region: str = "turkey",
) -> dict:
    """ROI tahmini."""
    return agent.handle({
        "action": "campaign_roi",
        "procedure": procedure,
        "budget_usd": budget_usd,
        "region": region,
    })


# ---------------------------------------------------------------------------
# Analytics Endpoints
# ---------------------------------------------------------------------------

@router.post("/analytics/report")
def analytics_report(body: AnalyticsReportRequest) -> dict:
    """Performans raporu."""
    return agent.get_analytics({
        "campaign_id": body.campaign_id,
        "period": body.period,
    })


@router.get("/analytics/funnel")
def analytics_funnel(period: str = "last_30d") -> dict:
    """Funnel metrikleri."""
    return agent.handle({
        "action": "analytics_funnel",
        "period": period,
    })


# ---------------------------------------------------------------------------
# Lead Endpoints
# ---------------------------------------------------------------------------

@router.post("/leads/segment")
def leads_segment(body: LeadSegmentRequest) -> dict:
    """Lead segmentasyonu."""
    return agent.optimize_funnel({
        "criteria": body.criteria,
        "region": body.region.value if body.region else None,
    })


@router.post("/leads/score")
def leads_score(body: LeadScoreRequest) -> dict:
    """Lead skorlama."""
    return agent.handle({
        "action": "lead_score",
        "source": body.source,
        "procedure_interest": body.procedure_interest,
        "budget_usd": body.budget_usd,
        "urgency": body.urgency,
        "region": body.region.value if body.region else None,
        "engagement_count": body.engagement_count,
    })


# ---------------------------------------------------------------------------
# Publish Endpoints
# ---------------------------------------------------------------------------

@router.post("/publish/schedule")
def publish_schedule(body: PublishRequest, db: Session = Depends(get_db)) -> dict:
    """Icerik zamanlama."""
    return agent.handle({
        "action": "publish_schedule",
        "content": body.content,
        "platform": body.platform.value,
        "publish_at": body.publish_at or "",
    }, db=db)


@router.post("/publish/now")
def publish_now(body: PublishRequest, db: Session = Depends(get_db)) -> dict:
    """Anlik yayinlama."""
    return agent.handle({
        "action": "publish_now",
        "content": body.content,
        "platform": body.platform.value,
    }, db=db)


@router.get("/publish/queue")
def publish_queue(db: Session = Depends(get_db)) -> dict:
    """Yayin kuyrugu."""
    return agent.handle({"action": "publish_queue"}, db=db)


# ---------------------------------------------------------------------------
# Info Endpoints
# ---------------------------------------------------------------------------

@router.get("/regions")
def list_regions() -> dict:
    """Desteklenen bolgeler & locale bilgisi."""
    return agent.handle({"action": "regions"})


@router.get("/platforms")
def list_platforms() -> dict:
    """Platform listesi & format kurallari."""
    return agent.handle({"action": "platforms"})
