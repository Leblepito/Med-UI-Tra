"""
AntiGravity Ventures — Skills: Commission Calculator
Medical referral komisyon hesaplama motoru.
"""
from __future__ import annotations

from dataclasses import dataclass

PROCEDURE_PRICES_USD: dict[str, float] = {
    "rhinoplasty": 4_500,
    "hair_transplant": 3_000,
    "dental_implant": 2_000,
    "dental_veneers": 1_500,
    "aesthetic_surgery": 5_500,
    "checkup": 600,
    "dermatology": 800,
    "eye_surgery": 2_500,
    "bariatric": 7_000,
    "ivf": 4_000,
}

DEFAULT_COMMISSION_RATE = 0.22   # 22%
VIP_COMMISSION_RATE = 0.25       # 25% for VIP / group referrals


@dataclass
class CommissionEstimate:
    procedure: str
    procedure_price_usd: float
    commission_rate: float
    commission_usd: float
    vip: bool

    def summary(self) -> str:
        tag = " [VIP]" if self.vip else ""
        return (
            f"{self.procedure.replace('_', ' ').title()}{tag}: "
            f"${self.procedure_price_usd:,.0f} × {self.commission_rate:.0%} "
            f"= ${self.commission_usd:,.2f} commission"
        )


def estimate(procedure: str, vip: bool = False, custom_price: float | None = None) -> CommissionEstimate:
    """Bir prosedür için komisyon hesaplar."""
    proc_key = procedure.lower().replace(" ", "_")
    price = custom_price or PROCEDURE_PRICES_USD.get(proc_key, 3_000)
    rate = VIP_COMMISSION_RATE if vip else DEFAULT_COMMISSION_RATE
    commission = round(price * rate, 2)
    return CommissionEstimate(
        procedure=proc_key,
        procedure_price_usd=price,
        commission_rate=rate,
        commission_usd=commission,
        vip=vip,
    )
