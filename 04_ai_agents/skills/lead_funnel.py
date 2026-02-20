"""
AntiGravity Ventures — Marketing: Lead Funnel & Segmentation
Lead skorlama, segmentasyon, remarketing ve nurture dizisi yonetimi.
"""
from __future__ import annotations

import uuid
from typing import Any


# ---------------------------------------------------------------------------
# Lead scoring weights
# ---------------------------------------------------------------------------
SCORE_WEIGHTS: dict[str, int] = {
    "has_budget": 20,
    "urgent": 15,
    "high_value_procedure": 15,
    "engaged": 10,
    "hot_region": 10,
    "returning_visitor": 10,
    "referral": 10,
    "form_complete": 10,
}

HIGH_VALUE_PROCEDURES = {"aesthetic", "ivf", "bariatric", "oncology"}
HOT_REGIONS = {"turkey", "russia", "uae"}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def segment_leads(leads: list[dict] | None, criteria: str = "all") -> dict[str, Any]:
    """Lead'leri segmentlere ayirir."""
    if not leads:
        # Demo data for MVP
        leads = _generate_sample_leads()

    segments = {"hot": [], "warm": [], "cold": []}

    for lead in leads:
        score_result = score_lead(lead)
        score = score_result["score"]
        lead_entry = {**lead, "score": score, "priority": score_result["priority"]}

        if score >= 70:
            segments["hot"].append(lead_entry)
        elif score >= 40:
            segments["warm"].append(lead_entry)
        else:
            segments["cold"].append(lead_entry)

    result = {
        "criteria": criteria,
        "total_leads": len(leads),
        "segments": {
            "hot": {"count": len(segments["hot"]), "leads": segments["hot"]},
            "warm": {"count": len(segments["warm"]), "leads": segments["warm"]},
            "cold": {"count": len(segments["cold"]), "leads": segments["cold"]},
        },
        "score_distribution": {
            "hot": len(segments["hot"]),
            "warm": len(segments["warm"]),
            "cold": len(segments["cold"]),
        },
    }

    if criteria == "procedure":
        result["by_procedure"] = _group_by(leads, "procedure_interest")
    elif criteria == "region":
        result["by_region"] = _group_by(leads, "region")

    return result


def generate_remarketing_list(segment: str, platform: str) -> dict[str, Any]:
    """Platform-specific audience tanimi olusturur."""
    audience_configs = {
        "google": {
            "hot": {"list_type": "Customer Match", "duration_days": 30, "bid_adjustment": "+25%"},
            "warm": {"list_type": "Website Visitors", "duration_days": 60, "bid_adjustment": "+10%"},
            "cold": {"list_type": "Similar Audiences", "duration_days": 90, "bid_adjustment": "0%"},
        },
        "meta": {
            "hot": {"list_type": "Custom Audience - Engaged", "lookalike_percent": 1, "bid_adjustment": "+20%"},
            "warm": {"list_type": "Custom Audience - Visitors", "lookalike_percent": 3, "bid_adjustment": "+5%"},
            "cold": {"list_type": "Lookalike Audience", "lookalike_percent": 5, "bid_adjustment": "0%"},
        },
        "yandex": {
            "hot": {"list_type": "Retargeting - Converters", "duration_days": 30, "bid_adjustment": "+30%"},
            "warm": {"list_type": "Retargeting - Visitors", "duration_days": 60, "bid_adjustment": "+10%"},
            "cold": {"list_type": "Look-alike", "duration_days": 90, "bid_adjustment": "0%"},
        },
    }

    config = audience_configs.get(platform.lower(), audience_configs["google"])
    segment_config = config.get(segment.lower(), config["cold"])

    return {
        "segment": segment,
        "platform": platform,
        "audience_config": segment_config,
        "recommendation": f"Use {segment_config['list_type']} targeting for {segment} leads on {platform}.",
    }


def suggest_ab_tests(page: str, current_metrics: dict | None = None) -> dict[str, Any]:
    """A/B test onerileri uretir."""
    tests = [
        {
            "element": "headline",
            "variant_a": "Current headline",
            "variant_b": "Benefit-focused headline with price anchor",
            "hypothesis": "Price-anchored headlines increase CTR by 15-25%",
            "priority": "high",
        },
        {
            "element": "cta_button",
            "variant_a": "Contact Us",
            "variant_b": "Get Free Quote",
            "hypothesis": "Action-specific CTAs convert 20-30% better than generic ones",
            "priority": "high",
        },
        {
            "element": "hero_image",
            "variant_a": "Hospital/clinic photo",
            "variant_b": "Before/after patient photo",
            "hypothesis": "Patient results images increase trust and conversion by 10-20%",
            "priority": "medium",
        },
        {
            "element": "social_proof",
            "variant_a": "No testimonials above fold",
            "variant_b": "Patient count + rating badge above fold",
            "hypothesis": "Social proof above fold reduces bounce rate by 8-15%",
            "priority": "medium",
        },
    ]

    return {
        "page": page,
        "current_metrics": current_metrics,
        "suggested_tests": tests,
        "recommended_duration": "14 days minimum per test",
        "min_sample_size": "1000 visitors per variant",
    }


def score_lead(lead_data: dict) -> dict[str, Any]:
    """Lead skorlama (0-100) + oncelik seviyesi."""
    score = 0
    factors = []

    # Budget factor
    budget = lead_data.get("budget_usd", 0) or 0
    if budget > 0:
        score += SCORE_WEIGHTS["has_budget"]
        factors.append(f"Has budget: ${budget}")
        if budget >= 5000:
            score += 5
            factors.append("High budget (>$5000)")

    # Urgency
    urgency = lead_data.get("urgency", "routine")
    if urgency in ("urgent", "emergency"):
        score += SCORE_WEIGHTS["urgent"]
        factors.append(f"Urgency: {urgency}")
    elif urgency == "soon":
        score += SCORE_WEIGHTS["urgent"] // 2
        factors.append("Moderate urgency")

    # High-value procedure
    proc = (lead_data.get("procedure_interest") or "").lower().replace(" ", "_").replace("-", "_")
    if proc in HIGH_VALUE_PROCEDURES:
        score += SCORE_WEIGHTS["high_value_procedure"]
        factors.append(f"High-value procedure: {proc}")

    # Engagement
    engagement = lead_data.get("engagement_count", 0) or 0
    if engagement >= 3:
        score += SCORE_WEIGHTS["engaged"]
        factors.append(f"High engagement ({engagement} interactions)")
    elif engagement >= 1:
        score += SCORE_WEIGHTS["engaged"] // 2
        factors.append("Some engagement")

    # Region
    region = (lead_data.get("region") or "").lower()
    if region in HOT_REGIONS:
        score += SCORE_WEIGHTS["hot_region"]
        factors.append(f"Hot region: {region}")

    # Source
    source = (lead_data.get("source") or "").lower()
    if "referral" in source or "whatsapp" in source:
        score += SCORE_WEIGHTS["referral"]
        factors.append(f"Referral source: {source}")

    score = min(100, max(0, score))

    if score >= 70:
        priority = "high"
        action = "Immediate follow-up — call or WhatsApp within 1 hour"
    elif score >= 40:
        priority = "medium"
        action = "Follow-up within 24 hours — send detailed info package"
    else:
        priority = "low"
        action = "Add to nurture email sequence — re-engage in 7 days"

    return {
        "score": score,
        "priority": priority,
        "factors": factors,
        "recommended_action": action,
    }


def generate_nurture_sequence(segment: str, lang: str) -> dict[str, Any]:
    """Email/WhatsApp nurture dizisi olusturur."""
    sequences = {
        "hot": {
            "en": [
                {"day": 0, "channel": "whatsapp", "message": "Thank you for your inquiry! A coordinator will contact you shortly."},
                {"day": 1, "channel": "email", "message": "Your personalized treatment plan is ready. Review it here."},
                {"day": 3, "channel": "whatsapp", "message": "Do you have any questions about the treatment plan we sent?"},
                {"day": 7, "channel": "email", "message": "Limited time: 10% discount on all-inclusive packages this month."},
            ],
            "tr": [
                {"day": 0, "channel": "whatsapp", "message": "Talebiniz icin tesekkurler! Koordinatorumuz en kisa surede sizinle iletisime gececek."},
                {"day": 1, "channel": "email", "message": "Kisisel tedavi planiniz hazir. Buradan inceleyebilirsiniz."},
                {"day": 3, "channel": "whatsapp", "message": "Gonderdigimiz tedavi plani hakkinda sorulariniz var mi?"},
                {"day": 7, "channel": "email", "message": "Sinirli sure: Bu ay tum paketlerde %10 indirim."},
            ],
            "ru": [
                {"day": 0, "channel": "whatsapp", "message": "Спасибо за обращение! Координатор свяжется с вами в ближайшее время."},
                {"day": 1, "channel": "email", "message": "Ваш персональный план лечения готов. Ознакомьтесь здесь."},
                {"day": 3, "channel": "whatsapp", "message": "Есть вопросы по плану лечения?"},
                {"day": 7, "channel": "email", "message": "Ограниченное предложение: скидка 10% на пакеты в этом месяце."},
            ],
        },
        "warm": {
            "en": [
                {"day": 0, "channel": "email", "message": "Thank you for your interest in medical tourism. Here's our guide."},
                {"day": 3, "channel": "email", "message": "See how our patients saved 50-70% on their procedures."},
                {"day": 7, "channel": "email", "message": "Ready to take the next step? Book a free consultation."},
                {"day": 14, "channel": "email", "message": "New patient success story: Read how [name] transformed their life."},
            ],
            "tr": [
                {"day": 0, "channel": "email", "message": "Saglik turizmine ilginiz icin tesekkurler. Rehberimizi inceleyin."},
                {"day": 3, "channel": "email", "message": "Hastalarimiz islemlerinde %50-70 nasil tasarruf etti gorun."},
                {"day": 7, "channel": "email", "message": "Bir sonraki adima hazir misiniz? Ucretsiz konsultasyon ayirtin."},
                {"day": 14, "channel": "email", "message": "Yeni hasta basari hikayesi: Hayatini nasil degistirdigini okuyun."},
            ],
            "ru": [
                {"day": 0, "channel": "email", "message": "Спасибо за интерес к медицинскому туризму. Вот наше руководство."},
                {"day": 3, "channel": "email", "message": "Узнайте, как наши пациенты сэкономили 50-70%."},
                {"day": 7, "channel": "email", "message": "Готовы к следующему шагу? Запишитесь на бесплатную консультацию."},
                {"day": 14, "channel": "email", "message": "Новая история успеха: Читайте, как пациент изменил свою жизнь."},
            ],
        },
        "cold": {
            "en": [
                {"day": 0, "channel": "email", "message": "Discover world-class healthcare at affordable prices."},
                {"day": 7, "channel": "email", "message": "5 reasons why medical tourists choose Turkey for treatment."},
                {"day": 21, "channel": "email", "message": "Special offer: Free consultation + travel planning assistance."},
            ],
            "tr": [
                {"day": 0, "channel": "email", "message": "Uygun fiyatlarla dunya standartlarinda saglik hizmeti kesfedin."},
                {"day": 7, "channel": "email", "message": "Saglik turistlerinin Turkiye'yi tercih etmesinin 5 nedeni."},
                {"day": 21, "channel": "email", "message": "Ozel teklif: Ucretsiz konsultasyon + seyahat planlama destegi."},
            ],
            "ru": [
                {"day": 0, "channel": "email", "message": "Откройте для себя медицину мирового уровня по доступным ценам."},
                {"day": 7, "channel": "email", "message": "5 причин, почему пациенты выбирают Турцию для лечения."},
                {"day": 21, "channel": "email", "message": "Специальное предложение: бесплатная консультация + помощь в планировании."},
            ],
        },
    }

    segment_key = segment.lower()
    seq = sequences.get(segment_key, sequences["cold"])
    messages = seq.get(lang, seq.get("en", []))

    return {
        "segment": segment,
        "lang": lang,
        "sequence_length": len(messages),
        "messages": messages,
        "estimated_duration_days": messages[-1]["day"] if messages else 0,
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _generate_sample_leads() -> list[dict]:
    """Demo lead verileri."""
    return [
        {"id": "L001", "source": "google_ads", "procedure_interest": "hair_transplant", "region": "turkey", "budget_usd": 3500, "urgency": "soon", "engagement_count": 4},
        {"id": "L002", "source": "instagram", "procedure_interest": "dental", "region": "europe", "budget_usd": 2000, "urgency": "routine", "engagement_count": 1},
        {"id": "L003", "source": "referral_whatsapp", "procedure_interest": "aesthetic", "region": "russia", "budget_usd": 8000, "urgency": "urgent", "engagement_count": 6},
        {"id": "L004", "source": "organic", "procedure_interest": "checkup", "region": "asia", "budget_usd": None, "urgency": "routine", "engagement_count": 0},
        {"id": "L005", "source": "yandex", "procedure_interest": "ivf", "region": "russia", "budget_usd": 6000, "urgency": "soon", "engagement_count": 3},
    ]


def _group_by(items: list[dict], key: str) -> dict[str, int]:
    groups: dict[str, int] = {}
    for item in items:
        val = str(item.get(key, "unknown"))
        groups[val] = groups.get(val, 0) + 1
    return groups
