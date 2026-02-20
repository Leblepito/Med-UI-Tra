"""
AntiGravity Ventures — Marketing AI Agent
SEO, icerik uretimi, kampanya planlama, analitik, lead funnel ve otomatik yayinlama.

Tum bolgeleri (Asya, Avrupa, BAE, Rusya, Turkiye) kapsayan locale-aware marketing motoru.
"""
from __future__ import annotations

import logging
from typing import Any

from skills import seo_engine, content_generator, campaign_manager
from skills import analytics_tracker, lead_funnel, auto_publisher

logger = logging.getLogger("MarketingAgent")


class MarketingAgent:
    """
    Sorumluluklar:
    - SEO keyword analizi & meta tag uretimi
    - Blog/reklam/sosyal medya icerik uretimi (RU/EN/TR/AR/TH)
    - Google Ads / Meta Ads / Yandex Direct kampanya planlamasi
    - Performans metrikleri & ROI hesaplama
    - Lead segmentasyonu & remarketing
    - Otomatik platform yayinlama
    """

    REGION_LOCALES: dict[str, dict[str, Any]] = {
        "turkey": {"lang": "tr", "currency": "USD", "platforms": ["google", "meta", "yandex"]},
        "russia": {"lang": "ru", "currency": "USD", "platforms": ["yandex", "vk", "meta"]},
        "uae":    {"lang": "ar", "currency": "AED", "platforms": ["google", "meta"]},
        "europe": {"lang": "en", "currency": "EUR", "platforms": ["google", "meta"]},
        "asia":   {"lang": "th", "currency": "THB", "platforms": ["google", "meta", "line"]},
    }

    def __init__(self) -> None:
        logger.info("MarketingAgent initialized — SEO | Content | Campaign | Analytics | Funnel | Publish")

    # ------------------------------------------------------------------
    # Main orchestrator entry point
    # ------------------------------------------------------------------

    def handle(self, request: dict[str, Any], db=None) -> dict[str, Any]:
        """Ana entry point — action bazli routing."""
        action = request.get("action", "status")
        logger.info(f"MarketingAgent handling action: {action}")

        # Store db on request for handlers that need it
        request["_db"] = db

        dispatch = {
            "seo_analyze": self.generate_seo_package,
            "seo_meta": self._generate_meta_tags,
            "content_blog": self._generate_blog,
            "content_ad": self._generate_ad_copy,
            "content_social": self._generate_social,
            "content_landing": self._generate_landing_page,
            "content_email": self._generate_email,
            "campaign_plan": self.plan_campaign,
            "campaign_budget": self._calculate_budget,
            "campaign_roi": self._estimate_roi,
            "analytics_report": self.get_analytics,
            "analytics_funnel": self._get_funnel,
            "lead_segment": self.optimize_funnel,
            "lead_score": self._score_lead,
            "publish_schedule": self._schedule_publish,
            "publish_now": self._publish_now,
            "publish_queue": self._get_queue,
            "regions": self._get_regions,
            "platforms": self._get_platforms,
            "status": self._status,
        }

        handler = dispatch.get(action, self._status)
        try:
            return handler(request)
        except Exception as e:
            logger.error(f"MarketingAgent error in {action}: {e}")
            return {"status": "error", "action": action, "message": str(e)}

    # ------------------------------------------------------------------
    # SEO
    # ------------------------------------------------------------------

    def generate_seo_package(self, request: dict[str, Any]) -> dict[str, Any]:
        """Keyword analizi + meta tag + SEO skor paketi."""
        procedure = request.get("procedure", "hair_transplant")
        region = request.get("region", "turkey")
        lang = request.get("lang") or self._default_lang(region)

        keyword_data = seo_engine.analyze_keywords(procedure, region, lang)
        keywords_list = [kw["keyword"] for kw in keyword_data.get("keywords", [])]

        meta_tags = seo_engine.generate_meta_tags(
            title=f"{procedure.replace('_', ' ').title()} — {region.title()}",
            description=f"Premium {procedure.replace('_', ' ')} in {region.title()}",
            keywords=keywords_list[:10],
            lang=lang,
        )

        sample_text = f"{procedure} {region} medical tourism premium treatment"
        score_data = seo_engine.score_content(sample_text, keywords_list[:5])

        return {
            "status": "ok",
            "action": "seo_analyze",
            **keyword_data,
            "meta_tags": meta_tags,
            "seo_score": score_data.get("seo_score", 0),
            "suggestions": score_data.get("suggestions", []),
        }

    def _generate_meta_tags(self, request: dict[str, Any]) -> dict[str, Any]:
        title = request.get("title", "")
        description = request.get("description", "")
        keywords = request.get("keywords", [])
        lang = request.get("lang", "en")

        tags = seo_engine.generate_meta_tags(title, description, keywords, lang)
        return {"status": "ok", "action": "seo_meta", "meta_tags": tags}

    # ------------------------------------------------------------------
    # Content Generation
    # ------------------------------------------------------------------

    def generate_content(self, request: dict[str, Any]) -> dict[str, Any]:
        """Icerik uretim yonlendiricisi."""
        content_type = request.get("content_type", "blog")
        dispatch = {
            "blog": self._generate_blog,
            "ad_copy": self._generate_ad_copy,
            "social": self._generate_social,
            "landing_page": self._generate_landing_page,
            "email": self._generate_email,
        }
        handler = dispatch.get(content_type, self._generate_blog)
        return handler(request)

    def _generate_blog(self, request: dict[str, Any]) -> dict[str, Any]:
        procedure = request.get("procedure", "hair_transplant")
        region = request.get("region", "turkey")
        lang = request.get("lang") or self._default_lang(region)
        tone = request.get("tone", "professional")

        result = content_generator.generate_blog_post(procedure, region, lang, tone)
        return {"status": "ok", "action": "content_blog", **result}

    def _generate_ad_copy(self, request: dict[str, Any]) -> dict[str, Any]:
        procedure = request.get("procedure", "hair_transplant")
        platform = request.get("platform", "google")
        region = request.get("region", "turkey")
        lang = request.get("lang") or self._default_lang(region)

        result = content_generator.generate_ad_copy(procedure, platform, region, lang)
        return {"status": "ok", "action": "content_ad", **result}

    def _generate_social(self, request: dict[str, Any]) -> dict[str, Any]:
        procedure = request.get("procedure", "hair_transplant")
        platform = request.get("platform", "instagram")
        region = request.get("region", "turkey")
        lang = request.get("lang") or self._default_lang(region)

        result = content_generator.generate_social_post(procedure, platform, region, lang)
        return {"status": "ok", "action": "content_social", **result}

    def _generate_landing_page(self, request: dict[str, Any]) -> dict[str, Any]:
        procedure = request.get("procedure", "hair_transplant")
        region = request.get("region", "turkey")
        lang = request.get("lang") or self._default_lang(region)

        result = content_generator.generate_landing_page_copy(procedure, region, lang)
        return {"status": "ok", "action": "content_landing", **result}

    def _generate_email(self, request: dict[str, Any]) -> dict[str, Any]:
        campaign_type = request.get("campaign_type", "welcome")
        region = request.get("region", "turkey")
        lang = request.get("lang") or self._default_lang(region)

        result = content_generator.generate_email_template(campaign_type, region, lang)
        return {"status": "ok", "action": "content_email", **result}

    # ------------------------------------------------------------------
    # Campaign Management
    # ------------------------------------------------------------------

    def plan_campaign(self, request: dict[str, Any]) -> dict[str, Any]:
        """Kampanya plani olusturur."""
        procedure = request.get("procedure", "hair_transplant")
        regions = request.get("regions", ["turkey"])
        budget_usd = request.get("budget_usd", 1000)
        duration_days = request.get("duration_days", 30)
        platforms = request.get("platforms")

        result = campaign_manager.plan_campaign(
            procedure=procedure,
            regions=regions,
            budget_usd=budget_usd,
            duration_days=duration_days,
            platforms=platforms,
        )
        return {"status": "ok", "action": "campaign_plan", **result}

    def _calculate_budget(self, request: dict[str, Any]) -> dict[str, Any]:
        total = request.get("total_budget", 1000)
        regions = request.get("regions", ["turkey"])
        platforms = request.get("platforms", ["google", "meta"])

        result = campaign_manager.calculate_budget_split(total, regions, platforms)
        return {"status": "ok", "action": "campaign_budget", "allocations": result}

    def _estimate_roi(self, request: dict[str, Any]) -> dict[str, Any]:
        procedure = request.get("procedure", "hair_transplant")
        budget = request.get("budget_usd", 1000)
        region = request.get("region", "turkey")

        result = campaign_manager.estimate_roi(procedure, budget, [region])
        return {"status": "ok", "action": "campaign_roi", **result}

    # ------------------------------------------------------------------
    # Analytics
    # ------------------------------------------------------------------

    def get_analytics(self, request: dict[str, Any]) -> dict[str, Any]:
        """Performans raporu."""
        campaign_id = request.get("campaign_id", "CMP-DEFAULT")
        period = request.get("period", "last_30d")

        result = analytics_tracker.create_report(campaign_id, period)
        return {"status": "ok", "action": "analytics_report", **result}

    def _get_funnel(self, request: dict[str, Any]) -> dict[str, Any]:
        period = request.get("period", "last_30d")
        result = analytics_tracker.get_funnel_metrics(period)
        return {"status": "ok", "action": "analytics_funnel", **result}

    # ------------------------------------------------------------------
    # Lead Funnel
    # ------------------------------------------------------------------

    def optimize_funnel(self, request: dict[str, Any]) -> dict[str, Any]:
        """Lead segmentasyonu."""
        criteria = request.get("criteria", "all")
        leads = request.get("leads")

        result = lead_funnel.segment_leads(leads, criteria)
        return {"status": "ok", "action": "lead_segment", **result}

    def _score_lead(self, request: dict[str, Any]) -> dict[str, Any]:
        lead_data = {
            "source": request.get("source", "organic"),
            "procedure_interest": request.get("procedure_interest", ""),
            "budget_usd": request.get("budget_usd"),
            "urgency": request.get("urgency", "routine"),
            "region": request.get("region"),
            "engagement_count": request.get("engagement_count", 0),
        }
        result = lead_funnel.score_lead(lead_data)
        return {"status": "ok", "action": "lead_score", **result}

    # ------------------------------------------------------------------
    # Auto Publisher
    # ------------------------------------------------------------------

    def auto_publish(self, request: dict[str, Any]) -> dict[str, Any]:
        """Otomatik yayinlama yonlendiricisi."""
        if request.get("publish_at"):
            return self._schedule_publish(request)
        return self._publish_now(request)

    def _schedule_publish(self, request: dict[str, Any]) -> dict[str, Any]:
        content = request.get("content", "")
        platform = request.get("platform", "google")
        publish_at = request.get("publish_at", "")
        db = request.get("_db")

        result = auto_publisher.schedule_post(content, platform, publish_at, db=db)
        return {"status": "ok", "action": "publish_schedule", **result}

    def _publish_now(self, request: dict[str, Any]) -> dict[str, Any]:
        content = request.get("content", "")
        platform = request.get("platform", "google")
        db = request.get("_db")

        result = auto_publisher.publish(content, platform, db=db)
        return {"status": "ok", "action": "publish_now", **result}

    def _get_queue(self, request: dict[str, Any]) -> dict[str, Any]:
        db = request.get("_db")
        result = auto_publisher.get_publish_queue(db=db)
        return {"status": "ok", "action": "publish_queue", **result}

    # ------------------------------------------------------------------
    # Info endpoints
    # ------------------------------------------------------------------

    def _get_regions(self, request: dict[str, Any]) -> dict[str, Any]:
        return {
            "status": "ok",
            "action": "regions",
            "regions": self.REGION_LOCALES,
            "total": len(self.REGION_LOCALES),
        }

    def _get_platforms(self, request: dict[str, Any]) -> dict[str, Any]:
        result = auto_publisher.get_supported_platforms()
        return {"status": "ok", "action": "platforms", **result}

    def _status(self, request: dict[str, Any] | None = None) -> dict[str, Any]:
        return {
            "agent": "MarketingAgent",
            "status": "active",
            "sector": "Marketing",
            "capabilities": [
                "seo_analyze", "seo_meta",
                "content_blog", "content_ad", "content_social",
                "content_landing", "content_email",
                "campaign_plan", "campaign_budget", "campaign_roi",
                "analytics_report", "analytics_funnel",
                "lead_segment", "lead_score",
                "publish_schedule", "publish_now", "publish_queue",
                "regions", "platforms",
            ],
            "supported_regions": list(self.REGION_LOCALES.keys()),
            "supported_languages": ["tr", "en", "ru", "ar", "th"],
        }

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _default_lang(self, region: str) -> str:
        """Bolge icin varsayilan dil."""
        return self.REGION_LOCALES.get(region.lower(), {}).get("lang", "en")
