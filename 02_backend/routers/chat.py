"""
AntiGravity Ventures — Chat Sector: FastAPI Router
/api/chat/* endpoints — AI Medical Secretary chatbot
"""
from __future__ import annotations

import logging
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database.connection import get_db

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
# In-memory session store (production would use DB)
# ---------------------------------------------------------------------------

_sessions: dict[str, dict] = {}


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
def start_session(body: StartSessionBody) -> dict:
    """Start a new chat session and get a greeting."""
    agent = _get_agent()
    session_id = f"chat-{uuid.uuid4().hex[:12]}"
    greeting = agent.get_greeting(body.language)

    _sessions[session_id] = {
        "language": body.language,
        "user_name": body.user_name,
        "messages": [],
        "created_at": datetime.utcnow().isoformat(),
    }

    return {
        "session_id": session_id,
        "greeting": greeting,
        "language": body.language,
    }


@router.post("/message", response_model=SendMessageResponse)
def send_message(body: SendMessageBody) -> dict:
    """Send a message and get an AI response."""
    agent = _get_agent()

    session = _sessions.get(body.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found. Start a new session first.")

    language = body.language or session["language"]

    # Add user message to history
    session["messages"].append({
        "role": "user",
        "content": body.message,
    })

    # Build messages for Claude (Anthropic format)
    claude_messages = [
        {"role": m["role"], "content": m["content"]}
        for m in session["messages"]
    ]

    # Call the agent
    try:
        result = agent.chat(
            messages=claude_messages,
            language=language,
            user_name=session.get("user_name"),
        )
    except RuntimeError as e:
        logger.error(f"Agent error: {e}")
        raise HTTPException(status_code=503, detail=str(e))

    # Add assistant response to history
    session["messages"].append({
        "role": "assistant",
        "content": result["response"],
    })

    # Keep conversation manageable (trim to last 50 turns)
    if len(session["messages"]) > 100:
        session["messages"] = session["messages"][-100:]

    message_id = f"msg-{uuid.uuid4().hex[:10]}"

    return {
        "session_id": body.session_id,
        "message_id": message_id,
        "response": result["response"],
        "tool_results": result.get("tool_results", []),
        "tokens_used": result.get("tokens", {}),
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/debug")
def debug_chat() -> dict:
    """Debug endpoint — check agent availability and API key."""
    import os
    has_key = bool(os.getenv("ANTHROPIC_API_KEY", ""))
    key_prefix = os.getenv("ANTHROPIC_API_KEY", "")[:12] + "..." if has_key else "NOT SET"
    try:
        from agents.chat_agent import MedicalSecretaryAgent, anthropic as anth_module
        agent_ok = True
        sdk_ok = anth_module is not None
    except Exception as e:
        agent_ok = False
        sdk_ok = False
        return {"agent_loaded": False, "error": str(e), "api_key": key_prefix}

    # Try creating client
    client_ok = False
    client_err = ""
    if sdk_ok and has_key:
        try:
            agent = MedicalSecretaryAgent()
            _ = agent.client  # triggers lazy init
            client_ok = True
        except Exception as e:
            client_err = str(e)

    return {
        "agent_loaded": agent_ok,
        "anthropic_sdk": sdk_ok,
        "api_key": key_prefix,
        "client_ok": client_ok,
        "client_error": client_err or None,
    }


@router.get("/history/{session_id}", response_model=HistoryResponse)
def get_history(session_id: str) -> dict:
    """Get chat history for a session."""
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "session_id": session_id,
        "messages": session["messages"],
        "total": len(session["messages"]),
    }
