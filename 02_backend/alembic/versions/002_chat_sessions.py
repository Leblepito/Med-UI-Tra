"""Add chat_sessions and chat_messages tables

Revision ID: 002_chat_sessions
Revises: 001_initial
Create Date: 2026-02-21
"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "002_chat_sessions"
down_revision = "001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "chat_sessions",
        sa.Column("session_id", sa.String(30), primary_key=True),
        sa.Column("language", sa.String(5), nullable=False, server_default="en"),
        sa.Column("user_name", sa.String(100), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "chat_messages",
        sa.Column("message_id", sa.String(30), primary_key=True),
        sa.Column("session_id", sa.String(30), sa.ForeignKey("chat_sessions.session_id"), nullable=False),
        sa.Column("role", sa.String(10), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_index("ix_chat_messages_session_id", "chat_messages", ["session_id"])


def downgrade() -> None:
    op.drop_index("ix_chat_messages_session_id", table_name="chat_messages")
    op.drop_table("chat_messages")
    op.drop_table("chat_sessions")
