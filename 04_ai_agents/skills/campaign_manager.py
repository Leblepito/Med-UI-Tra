"""
AntiGravity Ventures — Marketing: Campaign Manager
Google Ads / Meta Ads / Yandex Direct kampanya planlama, butce dagilimi ve ROI tahmini.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timedelta
from typing import Any


# ---------------------------------------------------------------------------
# Platform CPC tahminleri (USD, bolge bazli)
# ---------------------------------------------------------------------------
PLATFORM_CPC_ESTIMATES: dict[str, dict[str, float]] = {
    "google":  {"turkey": 0.45, "russia": 0.35, "uae": 1.20, "europe": 1.80, "asia": 0.60},
    "meta":    {"turkey": 0.25, "russia": 0.20, "uae": 0.80, "europe": 0.95, "asia": 0.40},
    "yandex":  {"russia": 0.30, "turkey": 0.40},
    "vk":      {"russia": 0.15},
    "line":    {"asia": 0.35},
}

# Ortalama donusum oranlari (prosedur bazli)
AVG_CONVERSION_RATES: dict[str, float] = {
    "hair_transplant": 0.035,
    "dental":          0.040,
    "aesthetic":       0.025,
    "bariatric":       0.020,
    "ivf":             0.015,
    "ophthalmology":   0.030,
    "checkup":         0.050,
    "dermatology":     0.035,
    "oncology":        0.010,
}

# Ortalama hasta basina gelir (USD)
AVG_REVENUE_PER_PATIENT: dict[str, float] = {
    "hair_transplant": 3000,
    "dental":          2000,
    "aesthetic":       5500,
    "bariatric":       4500,
    "ivf":             5000,
    "ophthalmology":   1500,
    "checkup":         600,
    "dermatology":     800,
    "oncology":        8000,
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def plan_campaign(
    procedure: str,
    regions: list[str],
    budget_usd: float,
    duration_days: int,
    platforms: list[str] | None = None,
) -> dict[str, Any]:
    """Tam kampanya plani olusturur: ad groups + butce + takvim + ROI."""
    proc_key = procedure.lower().replace(" ", "_").replace("-", "_")
    campaign_id = f"CMP-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

    if not platforms:
        platforms = ["google", "meta"]

    budget_split = calculate_budget_split(budget_usd, regions, platforms)
    ad_groups = generate_ad_groups(proc_key, regions)
    roi_estimate = estimate_roi(proc_key, budget_usd, regions)
    calendar = generate_campaign_calendar(campaign_id, duration_days)

    return {
        "campaign_id": campaign_id,
        "procedure": proc_key,
        "total_budget_usd": budget_usd,
        "duration_days": duration_days,
        "regions": regions,
        "platforms": platforms,
        "ad_groups": ad_groups,
        "budget_split": budget_split,
        "estimated_roi": roi_estimate,
        "calendar_summary": calendar,
        "status": "draft",
    }


def calculate_budget_split(
    total_budget: float,
    regions: list[str],
    platforms: list[str],
) -> list[dict[str, Any]]:
    """Bolge ve platform bazinda butce dagilimi hesaplar."""
    allocations = []
    # Weight by inverse CPC (cheaper regions get more budget for more clicks)
    entries = []
    for region in regions:
        for platform in platforms:
            cpc = _get_cpc(platform, region)
            if cpc > 0:
                entries.append({"region": region, "platform": platform, "cpc": cpc})

    if not entries:
        return []

    total_weight = sum(1.0 / e["cpc"] for e in entries)

    for e in entries:
        weight = (1.0 / e["cpc"]) / total_weight
        amount = round(total_budget * weight, 2)
        est_clicks = int(amount / e["cpc"]) if e["cpc"] > 0 else 0
        allocations.append({
            "region": e["region"],
            "platform": e["platform"],
            "amount_usd": amount,
            "estimated_clicks": est_clicks,
            "estimated_cpc": e["cpc"],
        })

    return allocations


def generate_ad_groups(procedure: str, regions: list[str]) -> list[dict[str, Any]]:
    """Prosedur ve bolge bazinda ad group yapisi olusturur."""
    groups = []
    for region in regions:
        groups.append({
            "name": f"{procedure}_{region}_broad",
            "match_type": "broad",
            "region": region,
            "targeting": f"Medical tourism interest + {region} location",
            "ad_count": 3,
        })
        groups.append({
            "name": f"{procedure}_{region}_exact",
            "match_type": "exact",
            "region": region,
            "targeting": f"Exact procedure keyword + {region} intent",
            "ad_count": 2,
        })
    return groups


def estimate_roi(
    procedure: str,
    budget_usd: float,
    regions: list[str] | None = None,
    custom_conversion_rate: float | None = None,
) -> dict[str, Any]:
    """Tahmini ROI, hasta sayisi ve gelir hesaplar."""
    proc_key = procedure.lower().replace(" ", "_").replace("-", "_")
    conv_rate = custom_conversion_rate or AVG_CONVERSION_RATES.get(proc_key, 0.025)
    revenue_per = AVG_REVENUE_PER_PATIENT.get(proc_key, 2000)

    # Weighted avg CPC across regions
    if regions:
        cpcs = [_get_cpc("google", r) for r in regions]
        avg_cpc = sum(cpcs) / max(len(cpcs), 1)
    else:
        avg_cpc = 0.80

    estimated_clicks = int(budget_usd / avg_cpc) if avg_cpc > 0 else 0
    estimated_leads = int(estimated_clicks * conv_rate)
    # ~30% of leads convert to patients
    estimated_patients = max(int(estimated_leads * 0.30), 0)
    estimated_revenue = estimated_patients * revenue_per
    commission_revenue = estimated_revenue * 0.22  # platform commission
    roi_percent = ((commission_revenue - budget_usd) / budget_usd * 100) if budget_usd > 0 else 0
    roas = commission_revenue / budget_usd if budget_usd > 0 else 0

    return {
        "budget_usd": budget_usd,
        "avg_cpc": round(avg_cpc, 2),
        "estimated_clicks": estimated_clicks,
        "estimated_leads": estimated_leads,
        "estimated_patients": estimated_patients,
        "estimated_revenue_usd": round(estimated_revenue, 2),
        "commission_revenue_usd": round(commission_revenue, 2),
        "roi_percent": round(roi_percent, 1),
        "roas": round(roas, 2),
        "conversion_rate": conv_rate,
    }


def generate_campaign_calendar(
    campaign_id: str,
    duration_days: int,
    start_date: str | None = None,
) -> str:
    """Kampanya takvim ozeti olusturur."""
    start = datetime.fromisoformat(start_date) if start_date else datetime.utcnow()
    end = start + timedelta(days=duration_days)

    weeks = max(duration_days // 7, 1)
    phases = []

    if weeks >= 4:
        phases = [
            f"Week 1-{min(2, weeks)}: Launch & data collection",
            f"Week {min(3, weeks)}-{min(4, weeks)}: Optimization & A/B testing",
            f"Week {min(5, weeks)}-{weeks}: Scale winning ads & reduce CPC",
        ]
    elif weeks >= 2:
        phases = [
            f"Week 1: Launch & data collection",
            f"Week 2-{weeks}: Optimize & scale",
        ]
    else:
        phases = [f"Day 1-{duration_days}: Sprint campaign — launch, optimize, convert"]

    return (
        f"Campaign: {campaign_id}\n"
        f"Start: {start.strftime('%Y-%m-%d')}\n"
        f"End: {end.strftime('%Y-%m-%d')}\n"
        f"Duration: {duration_days} days ({weeks} weeks)\n"
        f"Phases:\n" + "\n".join(f"  - {p}" for p in phases)
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_cpc(platform: str, region: str) -> float:
    """Platform + bolge bazli CPC dondurur."""
    plat = platform.lower().replace("_ads", "").replace("_direct", "")
    return PLATFORM_CPC_ESTIMATES.get(plat, {}).get(region.lower(), 0.50)
