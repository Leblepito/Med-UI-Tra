"""
AntiGravity Ventures — Marketing: Analytics Tracker
Performans metrikleri, ROI hesaplama, funnel takibi ve benchmark karsilastirma.
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any


# ---------------------------------------------------------------------------
# In-memory stores (Firestore'a tasinacak)
# ---------------------------------------------------------------------------
_conversion_log: list[dict[str, Any]] = []

# Industry benchmark averages for medical tourism
INDUSTRY_BENCHMARKS: dict[str, float] = {
    "ctr_percent": 3.2,
    "conversion_rate_percent": 2.8,
    "avg_cpc_usd": 0.85,
    "bounce_rate_percent": 42.0,
    "avg_session_duration_sec": 180,
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def create_report(campaign_id: str, period: str = "last_30d") -> dict[str, Any]:
    """Kampanya performans raporu olusturur (simulated data for MVP)."""
    # Simulated metrics — gercek entegrasyon Phase 2'de
    import random
    random.seed(hash(campaign_id + period) % 2**32)

    impressions = random.randint(5000, 50000)
    clicks = random.randint(int(impressions * 0.02), int(impressions * 0.06))
    ctr = round(clicks / max(impressions, 1) * 100, 2)
    avg_cpc = round(random.uniform(0.20, 2.00), 2)
    spend = round(clicks * avg_cpc, 2)
    conversions = random.randint(int(clicks * 0.01), int(clicks * 0.05))
    conv_rate = round(conversions / max(clicks, 1) * 100, 2)
    revenue = round(conversions * random.uniform(800, 5000), 2)
    roi = round((revenue - spend) / max(spend, 1) * 100, 1)
    roas = round(revenue / max(spend, 1), 2)

    return {
        "campaign_id": campaign_id,
        "period": period,
        "impressions": impressions,
        "clicks": clicks,
        "ctr": ctr,
        "avg_cpc": avg_cpc,
        "conversions": conversions,
        "conversion_rate": conv_rate,
        "spend_usd": spend,
        "revenue_usd": revenue,
        "roi_percent": roi,
        "roas": roas,
        "generated_at": datetime.utcnow().isoformat(),
        "note": "Simulated data — real analytics integration planned for Phase 2",
    }


def calculate_roi(spend: float, revenue: float) -> dict[str, Any]:
    """ROI ve ROAS hesaplar."""
    roi_percent = ((revenue - spend) / max(spend, 1)) * 100
    roas = revenue / max(spend, 1)
    profit = revenue - spend

    return {
        "spend_usd": round(spend, 2),
        "revenue_usd": round(revenue, 2),
        "profit_usd": round(profit, 2),
        "roi_percent": round(roi_percent, 1),
        "roas": round(roas, 2),
        "status": "profitable" if profit > 0 else "loss",
    }


def track_conversion(
    source: str,
    medium: str,
    campaign: str,
    patient_id: str | None = None,
) -> dict[str, Any]:
    """Donusum attribution kaydi olusturur."""
    record = {
        "conversion_id": f"CONV-{uuid.uuid4().hex[:8].upper()}",
        "source": source,
        "medium": medium,
        "campaign": campaign,
        "patient_id": patient_id,
        "timestamp": datetime.utcnow().isoformat(),
    }
    _conversion_log.append(record)
    return record


def get_funnel_metrics(period: str = "last_30d") -> dict[str, Any]:
    """Visitor -> Lead -> Consultation -> Patient funnel metrikleri."""
    # Simulated funnel data for MVP
    import random
    random.seed(hash(period) % 2**32)

    visitors = random.randint(2000, 15000)
    leads = int(visitors * random.uniform(0.03, 0.08))
    consultations = int(leads * random.uniform(0.20, 0.40))
    patients = int(consultations * random.uniform(0.25, 0.50))

    return {
        "period": period,
        "funnel": {
            "visitors": visitors,
            "leads": leads,
            "consultations": consultations,
            "patients": patients,
        },
        "conversion_rates": {
            "visitor_to_lead": round(leads / max(visitors, 1) * 100, 2),
            "lead_to_consultation": round(consultations / max(leads, 1) * 100, 2),
            "consultation_to_patient": round(patients / max(consultations, 1) * 100, 2),
            "overall": round(patients / max(visitors, 1) * 100, 3),
        },
        "generated_at": datetime.utcnow().isoformat(),
        "note": "Simulated data — real funnel tracking planned for Phase 2",
    }


def benchmark_compare(our_metrics: dict[str, float]) -> dict[str, Any]:
    """Kampanya metriklerini industry benchmark ile karsilastirir."""
    comparisons = {}
    for key, benchmark_val in INDUSTRY_BENCHMARKS.items():
        our_val = our_metrics.get(key)
        if our_val is not None:
            diff = round(our_val - benchmark_val, 2)
            status = "above_avg" if our_val > benchmark_val else "below_avg" if our_val < benchmark_val else "on_par"
            # For bounce rate, lower is better
            if "bounce" in key:
                status = "above_avg" if our_val < benchmark_val else "below_avg"
            comparisons[key] = {
                "our_value": our_val,
                "benchmark": benchmark_val,
                "difference": diff,
                "status": status,
            }

    return {
        "comparisons": comparisons,
        "overall_status": _overall_status(comparisons),
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _overall_status(comparisons: dict) -> str:
    above = sum(1 for v in comparisons.values() if v["status"] == "above_avg")
    total = len(comparisons)
    if total == 0:
        return "no_data"
    ratio = above / total
    if ratio >= 0.7:
        return "excellent"
    elif ratio >= 0.4:
        return "average"
    return "needs_improvement"
