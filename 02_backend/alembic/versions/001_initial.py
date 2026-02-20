"""Initial migration: 7 tables

Revision ID: 001_initial
Revises:
Create Date: 2026-02-21
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. hospitals
    op.create_table(
        "hospitals",
        sa.Column("hospital_id", sa.String(20), primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("city", sa.String(100), nullable=False),
        sa.Column("country", sa.String(50), nullable=False, server_default="Turkey"),
        sa.Column("specialties", ARRAY(sa.String), nullable=False),
        sa.Column("commission_rate", sa.Numeric(4, 3), nullable=False, server_default="0.22"),
        sa.Column("contact_whatsapp", sa.String(20), nullable=True),
        sa.Column("avg_procedure_cost_usd", sa.Numeric(10, 2), nullable=True),
        sa.Column("rating", sa.Numeric(2, 1), nullable=False, server_default="4.5"),
        sa.Column("languages", ARRAY(sa.String), nullable=False),
        sa.Column("jci_accredited", sa.Boolean, server_default="false"),
        sa.Column("active", sa.Boolean, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # 2. patients
    op.create_table(
        "patients",
        sa.Column("patient_id", sa.String(25), primary_key=True),
        sa.Column("full_name", sa.String(100), nullable=False),
        sa.Column("phone", sa.String(20), nullable=False),
        sa.Column("language", sa.String(5), nullable=False, server_default="ru"),
        sa.Column("procedure_interest", sa.String(200), nullable=False),
        sa.Column("procedure_category", sa.String(30), nullable=True),
        sa.Column("urgency", sa.String(15), server_default="routine"),
        sa.Column("budget_usd", sa.Numeric(10, 2), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("referral_source", sa.String(100), nullable=True),
        sa.Column("phuket_arrival_date", sa.Date, nullable=True),
        sa.Column("status", sa.String(30), server_default="inquiry"),
        sa.Column("matched_hospital_id", sa.String(20), sa.ForeignKey("hospitals.hospital_id"), nullable=True),
        sa.Column("estimated_procedure_cost_usd", sa.Numeric(10, 2), nullable=True),
        sa.Column("commission_rate", sa.Numeric(4, 3), nullable=True),
        sa.Column("commission_usd", sa.Numeric(10, 2), nullable=True),
        sa.Column("tags", ARRAY(sa.String), server_default="{}"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # 3. travel_requests
    op.create_table(
        "travel_requests",
        sa.Column("request_id", sa.String(25), primary_key=True),
        sa.Column("full_name", sa.String(100), nullable=False),
        sa.Column("phone", sa.String(20), nullable=False),
        sa.Column("language", sa.String(5), server_default="en"),
        sa.Column("destination", sa.String(100), nullable=True),
        sa.Column("check_in", sa.Date, nullable=True),
        sa.Column("check_out", sa.Date, nullable=True),
        sa.Column("guests", sa.Integer, server_default="2"),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("status", sa.String(20), server_default="new"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # 4. campaigns
    op.create_table(
        "campaigns",
        sa.Column("campaign_id", sa.String(25), primary_key=True),
        sa.Column("procedure", sa.String(50), nullable=False),
        sa.Column("regions", ARRAY(sa.String), nullable=False),
        sa.Column("platforms", ARRAY(sa.String), nullable=False),
        sa.Column("total_budget_usd", sa.Numeric(10, 2), nullable=False),
        sa.Column("duration_days", sa.Integer, server_default="30"),
        sa.Column("status", sa.String(20), server_default="draft"),
        sa.Column("budget_split", JSONB, nullable=True),
        sa.Column("ad_groups", JSONB, nullable=True),
        sa.Column("estimated_roi", JSONB, nullable=True),
        sa.Column("calendar_summary", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # 5. leads
    op.create_table(
        "leads",
        sa.Column("lead_id", sa.String(25), primary_key=True),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("procedure_interest", sa.String(100), nullable=False),
        sa.Column("region", sa.String(30), nullable=True),
        sa.Column("budget_usd", sa.Numeric(10, 2), nullable=True),
        sa.Column("urgency", sa.String(15), server_default="routine"),
        sa.Column("engagement_count", sa.Integer, server_default="0"),
        sa.Column("score", sa.Integer, nullable=True),
        sa.Column("priority", sa.String(10), nullable=True),
        sa.Column("patient_id", sa.String(25), sa.ForeignKey("patients.patient_id"), nullable=True),
        sa.Column("campaign_id", sa.String(25), sa.ForeignKey("campaigns.campaign_id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # 6. publish_queue
    op.create_table(
        "publish_queue",
        sa.Column("post_id", sa.String(20), primary_key=True),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("platform", sa.String(20), nullable=False),
        sa.Column("region", sa.String(30), nullable=True),
        sa.Column("lang", sa.String(5), nullable=True),
        sa.Column("status", sa.String(20), server_default="scheduled"),
        sa.Column("publish_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("campaign_id", sa.String(25), sa.ForeignKey("campaigns.campaign_id"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # 7. conversions
    op.create_table(
        "conversions",
        sa.Column("conversion_id", sa.String(20), primary_key=True),
        sa.Column("source", sa.String(50), nullable=False),
        sa.Column("medium", sa.String(50), nullable=False),
        sa.Column("campaign", sa.String(100), nullable=False),
        sa.Column("patient_id", sa.String(25), sa.ForeignKey("patients.patient_id"), nullable=True),
        sa.Column("campaign_id", sa.String(25), sa.ForeignKey("campaigns.campaign_id"), nullable=True),
        sa.Column("revenue_usd", sa.Numeric(10, 2), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("conversions")
    op.drop_table("publish_queue")
    op.drop_table("leads")
    op.drop_table("campaigns")
    op.drop_table("travel_requests")
    op.drop_table("patients")
    op.drop_table("hospitals")
