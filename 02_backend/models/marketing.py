"""
AntiGravity Ventures — Marketing Sector: Pydantic v2 Data Models
SEO, kampanya, lead funnel, analitik ve yayinlama modelleri.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class Region(str, Enum):
    TURKEY = "turkey"
    RUSSIA = "russia"
    UAE = "uae"
    EUROPE = "europe"
    ASIA = "asia"


class Platform(str, Enum):
    GOOGLE = "google"
    META = "meta"
    YANDEX = "yandex"
    VK = "vk"
    INSTAGRAM = "instagram"
    LINE = "line"


class ContentType(str, Enum):
    BLOG = "blog"
    AD_COPY = "ad_copy"
    SOCIAL = "social"
    LANDING_PAGE = "landing_page"
    EMAIL = "email"


class CampaignStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class LeadScore(str, Enum):
    HOT = "hot"
    WARM = "warm"
    COLD = "cold"


# ---------------------------------------------------------------------------
# Request Models
# ---------------------------------------------------------------------------

class SEOAnalyzeRequest(BaseModel):
    """Keyword analizi ve SEO skoru istegi."""
    procedure: str = Field(..., min_length=1, description="Prosedur adi (orn: hair_transplant)")
    region: Region = Field(Region.TURKEY)
    lang: str = Field("en", pattern=r"^(tr|en|ru|ar|th)$")


class MetaTagRequest(BaseModel):
    """Meta tag uretimi istegi."""
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    keywords: list[str] = Field(default_factory=list)
    lang: str = Field("en", pattern=r"^(tr|en|ru|ar|th)$")


class ContentRequest(BaseModel):
    """Icerik uretimi istegi (blog, reklam, sosyal medya)."""
    content_type: ContentType = Field(ContentType.BLOG)
    procedure: str = Field(..., min_length=1)
    platform: Optional[Platform] = None
    region: Region = Field(Region.TURKEY)
    lang: str = Field("en", pattern=r"^(tr|en|ru|ar|th)$")
    tone: str = Field("professional", pattern=r"^(professional|casual|urgent|luxury)$")


class CampaignPlanRequest(BaseModel):
    """Kampanya planlama istegi."""
    procedure: str = Field(..., min_length=1)
    regions: list[Region] = Field(default_factory=lambda: [Region.TURKEY])
    budget_usd: float = Field(..., gt=0, description="Toplam butce (USD)")
    duration_days: int = Field(30, ge=1, le=365)
    platforms: list[Platform] = Field(default_factory=lambda: [Platform.GOOGLE, Platform.META])


class BudgetSplitRequest(BaseModel):
    """Butce dagilimi hesaplama istegi."""
    total_budget: float = Field(..., gt=0)
    regions: list[Region] = Field(default_factory=lambda: [Region.TURKEY])
    platforms: list[Platform] = Field(default_factory=lambda: [Platform.GOOGLE, Platform.META])


class ROIEstimateRequest(BaseModel):
    """ROI tahmini istegi."""
    procedure: str = Field(..., min_length=1)
    budget_usd: float = Field(..., gt=0)
    region: Region = Field(Region.TURKEY)


class AnalyticsReportRequest(BaseModel):
    """Performans raporu istegi."""
    campaign_id: str = Field(..., min_length=1)
    period: str = Field("last_30d", pattern=r"^(last_7d|last_30d|last_90d|custom)$")


class LeadSegmentRequest(BaseModel):
    """Lead segmentasyonu istegi."""
    criteria: str = Field("procedure", pattern=r"^(procedure|region|score|all)$")
    region: Optional[Region] = None


class LeadScoreRequest(BaseModel):
    """Lead skorlama istegi."""
    source: str = Field(..., min_length=1)
    procedure_interest: str = Field(..., min_length=1)
    budget_usd: Optional[float] = Field(None, ge=0)
    urgency: str = Field("routine", pattern=r"^(routine|soon|urgent|emergency)$")
    region: Optional[Region] = None
    engagement_count: int = Field(0, ge=0)


class PublishRequest(BaseModel):
    """Icerik yayinlama / zamanlama istegi."""
    content: str = Field(..., min_length=1)
    platform: Platform
    region: Region = Field(Region.TURKEY)
    lang: str = Field("en", pattern=r"^(tr|en|ru|ar|th)$")
    publish_at: Optional[str] = Field(None, description="ISO datetime veya None (hemen yayinla)")


# ---------------------------------------------------------------------------
# Response Models
# ---------------------------------------------------------------------------

class KeywordInfo(BaseModel):
    keyword: str
    search_volume_estimate: str
    difficulty: str
    cpc_estimate: float


class SEOPackage(BaseModel):
    """SEO analiz sonucu."""
    procedure: str
    region: str
    lang: str
    keywords: list[KeywordInfo]
    meta_tags: dict
    seo_score: int = Field(ge=0, le=100)
    suggestions: list[str]


class GeneratedContent(BaseModel):
    """Uretilen icerik."""
    content_type: str
    title: str
    body: str
    meta: Optional[dict] = None
    cta: str
    platform_formatted: Optional[dict] = None
    lang: str
    region: str


class BudgetAllocation(BaseModel):
    region: str
    platform: str
    amount_usd: float
    estimated_clicks: int
    estimated_cpc: float


class CampaignPlan(BaseModel):
    """Kampanya plani."""
    campaign_id: str
    procedure: str
    total_budget_usd: float
    duration_days: int
    ad_groups: list[dict]
    budget_split: list[BudgetAllocation]
    estimated_roi: dict
    calendar_summary: str


class AnalyticsReport(BaseModel):
    """Performans raporu."""
    campaign_id: str
    period: str
    impressions: int
    clicks: int
    ctr: float
    avg_cpc: float
    conversions: int
    conversion_rate: float
    spend_usd: float
    revenue_usd: float
    roi_percent: float
    roas: float


class LeadSegment(BaseModel):
    """Segmentasyon sonucu."""
    segment_id: str
    name: str
    criteria: str
    lead_count: int
    score_distribution: dict
    remarketing_suggestion: str


class LeadScoreResult(BaseModel):
    """Lead skor sonucu."""
    score: int = Field(ge=0, le=100)
    priority: str
    factors: list[str]
    recommended_action: str


class PublishResult(BaseModel):
    """Yayinlama sonucu."""
    status: str
    platform: str
    formatted_content: str
    scheduled_at: Optional[str] = None
    publish_queue_position: Optional[int] = None
