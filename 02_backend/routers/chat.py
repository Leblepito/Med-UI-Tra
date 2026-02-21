"""
AntiGravity Ventures — Chat Sector: FastAPI Router
/api/chat/* endpoints — AI Medical Secretary chatbot
DB-persisted sessions & messages.
"""
from __future__ import annotations

import logging
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database.connection import get_db
from database.models import ChatSession, ChatMessage

# Rate limiting (graceful — works even without slowapi)
try:
    from slowapi import Limiter
    from slowapi.util import get_remote_address
    limiter = Limiter(key_func=get_remote_address)
    _has_limiter = True
except ImportError:
    _has_limiter = False

logger = logging.getLogger("thaiturk.chat")

# Agent path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "04_ai_agents"))

try:
    from agents.chat_agent import MedicalSecretaryAgent
except ImportError:
    MedicalSecretaryAgent = None  # type: ignore[assignment,misc]

router = APIRouter(prefix="/api/chat", tags=["Chat"])

# Singleton agent instance
_agent: MedicalSecretaryAgent | None = None


def _get_agent() -> MedicalSecretaryAgent:
    global _agent
    if _agent is None:
        if MedicalSecretaryAgent is None:
            raise HTTPException(status_code=503, detail="Chat agent not available")
        _agent = MedicalSecretaryAgent()
    return _agent


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------

class StartSessionBody(BaseModel):
    language: str = Field("en", description="Language code: ru, tr, en, th, ar, zh")
    user_name: Optional[str] = Field(None, max_length=100)


class StartSessionResponse(BaseModel):
    session_id: str
    greeting: str
    language: str


class SendMessageBody(BaseModel):
    session_id: str = Field(..., description="Session ID from start_session")
    message: str = Field(..., min_length=1, max_length=2000)
    language: Optional[str] = Field(None, description="Override language for this message")


class SendMessageResponse(BaseModel):
    session_id: str
    message_id: str
    response: str
    tool_results: list[dict] = []
    tokens_used: dict = {}
    timestamp: str


class HistoryResponse(BaseModel):
    session_id: str
    messages: list[dict]
    total: int


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/session", response_model=StartSessionResponse)
def start_session(body: StartSessionBody, request: Request, db: Session = Depends(get_db)) -> dict:
    """Start a new chat session and get a greeting."""
    agent = _get_agent()
    session_id = f"chat-{uuid.uuid4().hex[:12]}"
    greeting = agent.get_greeting(body.language)

    # Persist session to DB
    db_session = ChatSession(
        session_id=session_id,
        language=body.language,
        user_name=body.user_name,
    )
    db.add(db_session)

    # Persist greeting as first message
    greeting_msg = ChatMessage(
        message_id=f"msg-{uuid.uuid4().hex[:10]}",
        session_id=session_id,
        role="assistant",
        content=greeting,
    )
    db.add(greeting_msg)
    db.commit()

    return {
        "session_id": session_id,
        "greeting": greeting,
        "language": body.language,
    }


@router.post("/message", response_model=SendMessageResponse)
@(limiter.limit("20/minute") if _has_limiter else lambda f: f)
def send_message(body: SendMessageBody, request: Request, db: Session = Depends(get_db)) -> dict:
    """Send a message and get an AI response."""
    agent = _get_agent()

    db_session = db.query(ChatSession).filter(ChatSession.session_id == body.session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found. Start a new session first.")

    language = body.language or db_session.language

    # Persist user message
    user_msg_id = f"msg-{uuid.uuid4().hex[:10]}"
    user_msg = ChatMessage(
        message_id=user_msg_id,
        session_id=body.session_id,
        role="user",
        content=body.message,
    )
    db.add(user_msg)
    db.flush()

    # Build messages for Claude (last 100 messages for context window)
    recent_messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == body.session_id)
        .order_by(ChatMessage.created_at)
        .limit(100)
        .all()
    )
    claude_messages = [
        {"role": m.role, "content": m.content}
        for m in recent_messages
    ]

    # Call the agent
    try:
        result = agent.chat(
            messages=claude_messages,
            language=language,
            user_name=db_session.user_name,
        )
    except RuntimeError as e:
        logger.error(f"Agent error: {e}")
        db.rollback()
        raise HTTPException(status_code=503, detail=str(e))

    # Persist assistant response
    assistant_msg_id = f"msg-{uuid.uuid4().hex[:10]}"
    assistant_msg = ChatMessage(
        message_id=assistant_msg_id,
        session_id=body.session_id,
        role="assistant",
        content=result["response"],
    )
    db.add(assistant_msg)
    db.commit()

    return {
        "session_id": body.session_id,
        "message_id": assistant_msg_id,
        "response": result["response"],
        "tool_results": result.get("tool_results", []),
        "tokens_used": result.get("tokens", {}),
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/history/{session_id}", response_model=HistoryResponse)
def get_history(session_id: str, db: Session = Depends(get_db)) -> dict:
    """Get chat history for a session."""
    db_session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
        .all()
    )

    return {
        "session_id": session_id,
        "messages": [m.to_dict() for m in messages],
        "total": len(messages),
    }
