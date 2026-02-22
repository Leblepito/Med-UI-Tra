"""
AntiGravity Ventures — SQLAlchemy ORM Models
11 tables: hospitals, patients, travel_requests, campaigns, leads, publish_queue, conversions, chat_sessions, chat_messages, visualizations, users.
"""
from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import relationship

from database.connection import Base


# ---------------------------------------------------------------------------
# 1. hospitals
# ---------------------------------------------------------------------------

class Hospital(Base):
    __tablename__ = "hospitals"

    hospital_id = Column(String(20), primary_key=True)
    name = Column(String(200), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(50), nullable=False, server_default="Turkey")
    specialties = Column(ARRAY(String), nullable=False)
    commission_rate = Column(Numeric(4, 3), nullable=False, server_default="0.22")
    contact_whatsapp = Column(String(20), nullable=True)
    avg_procedure_cost_usd = Column(Numeric(10, 2), nullable=True)
    rating = Column(Numeric(2, 1), nullable=False, server_default="4.5")
    languages = Column(ARRAY(String), nullable=False)
    jci_accredited = Column(Boolean, server_default="false")
    active = Column(Boolean, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    patients = relationship("Patient", back_populates="hospital")

    def to_dict(self) -> dict:
        return {
            "hospital_id": self.hospital_id,
            "name": self.name,
            "city": self.city,
            "country": self.country,
            "specialties": self.specialties or [],
            "commission_rate": float(self.commission_rate) if self.commission_rate else 0.22,
            "contact_whatsapp": self.contact_whatsapp,
            "avg_procedure_cost_usd": float(self.avg_procedure_cost_usd) if self.avg_procedure_cost_usd else None,
            "rating": float(self.rating) if self.rating else 4.5,
            "languages": self.languages or [],
            "jci_accredited": self.jci_accredited or False,
            "active": self.active if self.active is not None else True,
        }


# ---------------------------------------------------------------------------
# 2. patients
# ---------------------------------------------------------------------------

class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(String(25), primary_key=True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    language = Column(String(5), nullable=False, server_default="ru")
    procedure_interest = Column(String(200), nullable=False)
    procedure_category = Column(String(30), nullable=True)
    urgency = Column(String(15), server_default="routine")
    budget_usd = Column(Numeric(10, 2), nullable=True)
    notes = Column(Text, nullable=True)
    referral_source = Column(String(100), nullable=True)
    phuket_arrival_date = Column(Date, nullable=True)
    status = Column(String(30), server_default="inquiry")
    matched_hospital_id = Column(String(20), ForeignKey("hospitals.hospital_id"), nullable=True)
    estimated_procedure_cost_usd = Column(Numeric(10, 2), nullable=True)
    commission_rate = Column(Numeric(4, 3), nullable=True)
    commission_usd = Column(Numeric(10, 2), nullable=True)
    tags = Column(ARRAY(String), server_default="{}")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    hospital = relationship("Hospital", back_populates="patients")
    leads = relationship("Lead", back_populates="patient")
    conversions = relationship("Conversion", back_populates="patient")

    def to_dict(self) -> dict:
        return {
            "patient_id": self.patient_id,
            "intake": {
                "full_name": self.full_name,
                "phone": self.phone,
                "language": self.language,
                "procedure_interest": self.procedure_interest,
                "urgency": self.urgency,
                "budget_usd": float(self.budget_usd) if self.budget_usd else None,
                "notes": self.notes,
                "referral_source": self.referral_source,
                "phuket_arrival_date": self.phuket_arrival_date.isoformat() if self.phuket_arrival_date else None,
            },
            "procedure_category": self.procedure_category,
            "status": self.status,
            "matched_hospital": self.matched_hospital_id,
            "estimated_procedure_cost_usd": float(self.estimated_procedure_cost_usd) if self.estimated_procedure_cost_usd else None,
            "commission_rate": float(self.commission_rate) if self.commission_rate else None,
            "commission_usd": float(self.commission_usd) if self.commission_usd else None,
            "tags": self.tags or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


# ---------------------------------------------------------------------------
# 3. travel_requests
# ---------------------------------------------------------------------------

class TravelRequest(Base):
    __tablename__ = "travel_requests"

    request_id = Column(String(25), primary_key=True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)
    language = Column(String(5), server_default="en")
    destination = Column(String(100), nullable=True)
    check_in = Column(Date, nullable=True)
    check_out = Column(Date, nullable=True)
    guests = Column(Integer, server_default="2")
    notes = Column(Text, nullable=True)
    status = Column(String(20), server_default="new")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


# ---------------------------------------------------------------------------
# 4. campaigns
# ---------------------------------------------------------------------------

class Campaign(Base):
    __tablename__ = "campaigns"

    campaign_id = Column(String(25), primary_key=True)
    procedure = Column(String(50), nullable=False)
    regions = Column(ARRAY(String), nullable=False)
    platforms = Column(ARRAY(String), nullable=False)
    total_budget_usd = Column(Numeric(10, 2), nullable=False)
    duration_days = Column(Integer, server_default="30")
    status = Column(String(20), server_default="draft")
    budget_split = Column(JSONB, nullable=True)
    ad_groups = Column(JSONB, nullable=True)
    estimated_roi = Column(JSONB, nullable=True)
    calendar_summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    leads = relationship("Lead", back_populates="campaign")
    posts = relationship("PublishQueueItem", back_populates="campaign")
    conversions = relationship("Conversion", back_populates="campaign_ref")


# ---------------------------------------------------------------------------
# 5. leads
# ---------------------------------------------------------------------------

class Lead(Base):
    __tablename__ = "leads"

    lead_id = Column(String(25), primary_key=True)
    source = Column(String(50), nullable=False)
    procedure_interest = Column(String(100), nullable=False)
    region = Column(String(30), nullable=True)
    budget_usd = Column(Numeric(10, 2), nullable=True)
    urgency = Column(String(15), server_default="routine")
    engagement_count = Column(Integer, server_default="0")
    score = Column(Integer, nullable=True)
    priority = Column(String(10), nullable=True)
    patient_id = Column(String(25), ForeignKey("patients.patient_id"), nullable=True)
    campaign_id = Column(String(25), ForeignKey("campaigns.campaign_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    patient = relationship("Patient", back_populates="leads")
    campaign = relationship("Campaign", back_populates="leads")


# ---------------------------------------------------------------------------
# 6. publish_queue
# ---------------------------------------------------------------------------

class PublishQueueItem(Base):
    __tablename__ = "publish_queue"

    post_id = Column(String(20), primary_key=True)
    content = Column(Text, nullable=False)
    platform = Column(String(20), nullable=False)
    region = Column(String(30), nullable=True)
    lang = Column(String(5), nullable=True)
    status = Column(String(20), server_default="scheduled")
    publish_at = Column(DateTime(timezone=True), nullable=True)
    published_at = Column(DateTime(timezone=True), nullable=True)
    campaign_id = Column(String(25), ForeignKey("campaigns.campaign_id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    campaign = relationship("Campaign", back_populates="posts")

    def to_dict(self) -> dict:
        return {
            "post_id": self.post_id,
            "content": self.content,
            "platform": self.platform,
            "region": self.region,
            "lang": self.lang,
            "status": self.status,
            "publish_at": self.publish_at.isoformat() if self.publish_at else None,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "campaign_id": self.campaign_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ---------------------------------------------------------------------------
# 7. conversions
# ---------------------------------------------------------------------------

class Conversion(Base):
    __tablename__ = "conversions"

    conversion_id = Column(String(20), primary_key=True)
    source = Column(String(50), nullable=False)
    medium = Column(String(50), nullable=False)
    campaign = Column(String(100), nullable=False)
    patient_id = Column(String(25), ForeignKey("patients.patient_id"), nullable=True)
    campaign_id = Column(String(25), ForeignKey("campaigns.campaign_id"), nullable=True)
    revenue_usd = Column(Numeric(10, 2), nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    patient = relationship("Patient", back_populates="conversions")
    campaign_ref = relationship("Campaign", back_populates="conversions")

    def to_dict(self) -> dict:
        return {
            "conversion_id": self.conversion_id,
            "source": self.source,
            "medium": self.medium,
            "campaign": self.campaign,
            "patient_id": self.patient_id,
            "campaign_id": self.campaign_id,
            "revenue_usd": float(self.revenue_usd) if self.revenue_usd else None,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
        }


# ---------------------------------------------------------------------------
# 8. chat_sessions
# ---------------------------------------------------------------------------

class ChatSession(Base):
    __tablename__ = "chat_sessions"

    session_id = Column(String(30), primary_key=True)
    language = Column(String(5), nullable=False, server_default="en")
    user_name = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    messages = relationship("ChatMessage", back_populates="session", order_by="ChatMessage.created_at")

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "language": self.language,
            "user_name": self.user_name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ---------------------------------------------------------------------------
# 9. chat_messages
# ---------------------------------------------------------------------------

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    message_id = Column(String(30), primary_key=True)
    session_id = Column(String(30), ForeignKey("chat_sessions.session_id"), nullable=False)
    role = Column(String(10), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    session = relationship("ChatSession", back_populates="messages")

    def to_dict(self) -> dict:
        return {
            "message_id": self.message_id,
            "role": self.role,
            "content": self.content,
            "timestamp": self.created_at.isoformat() if self.created_at else None,
        }


# ---------------------------------------------------------------------------
# 10. visualizations (Meshy.ai Before/After)
# ---------------------------------------------------------------------------

class Visualization(Base):
    __tablename__ = "visualizations"

    viz_id = Column(String(25), primary_key=True)
    ip_address = Column(String(45), nullable=False)
    procedure_category = Column(String(50), nullable=False)
    questions_answers = Column(JSONB, nullable=True)
    meshy_task_id = Column(String(100), nullable=True)
    status = Column(String(20), nullable=False, server_default="pending")
    input_image_b64 = Column(Text, nullable=False)
    output_image_url = Column(Text, nullable=True)
    post_op_image_b64 = Column(Text, nullable=True)
    similarity_score = Column(Numeric(5, 2), nullable=True)
    meshy_response = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def to_dict(self) -> dict:
        return {
            "viz_id": self.viz_id,
            "procedure_category": self.procedure_category,
            "status": self.status,
            "output_image_url": self.output_image_url,
            "similarity_score": float(self.similarity_score) if self.similarity_score else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ---------------------------------------------------------------------------
# 11. users (Auth)
# ---------------------------------------------------------------------------

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(200), nullable=True)
    role = Column(String(20), nullable=False, server_default="staff")  # admin | staff | coordinator
    is_active = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
