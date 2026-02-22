"""
AntiGravity Ventures — ThaiTurk Backend
FastAPI entry point.
"""
from __future__ import annotations

import logging
import os
import traceback
from contextlib import asynccontextmanager
from pathlib import Path
import sys

from dotenv import load_dotenv

# Load .env before anything reads env vars
load_dotenv(Path(__file__).parent / ".env", override=False)

# Logging setup
logging.basicConfig(
    level=logging.DEBUG if os.getenv("ENVIRONMENT", "development") != "production" else logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%H:%M:%S",
)

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from database.connection import Base, engine
from database import models  # noqa: F401  — register all ORM models

logger = logging.getLogger("thaiturk")

# ---------------------------------------------------------------------------
# Env validation
# ---------------------------------------------------------------------------

_env = os.getenv("ENVIRONMENT", "development")
_is_production = _env == "production"

_REQUIRED_ENV_VARS_PROD = ["DATABASE_URL", "ANTHROPIC_API_KEY", "API_SECRET_KEY"]


def _validate_env() -> None:
    """Check required env vars at startup. Fail fast in production."""
    missing = [v for v in _REQUIRED_ENV_VARS_PROD if not os.getenv(v)]
    if missing and _is_production:
        msg = f"Missing required environment variables: {', '.join(missing)}"
        logger.critical(msg)
        raise RuntimeError(msg)
    elif missing:
        logger.warning(f"Missing env vars (ok for dev): {', '.join(missing)}")


_validate_env()

# ---------------------------------------------------------------------------
# Agent imports
# ---------------------------------------------------------------------------

_agents_path = Path(__file__).parent.parent / "04_ai_agents"
if _agents_path.exists():
    sys.path.insert(0, str(_agents_path))

try:
    from master_orchestrator import AgentRouter  # noqa: E402
except ImportError:
    class AgentRouter:
        def route(self, payload: dict) -> dict:
            return {"status": "ok", "message": "Orchestrator not available", "payload": payload}


from routers.medical import router as medical_router  # noqa: E402
from routers.travel import router as travel_router  # noqa: E402
from routers.marketing import router as marketing_router  # noqa: E402
from routers.chat import router as chat_router  # noqa: E402
from routers.blog import router as blog_router  # noqa: E402
from routers.meshy import router as meshy_router  # noqa: E402
from routers.auth import router as auth_router  # noqa: E402
from routers.notification import router as notification_router  # noqa: E402
from auth import require_admin  # noqa: E402

# ---------------------------------------------------------------------------
# Rate limiting
# ---------------------------------------------------------------------------

try:
    from slowapi import Limiter, _rate_limit_exceeded_handler
    from slowapi.util import get_remote_address
    from slowapi.errors import RateLimitExceeded

    limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])
    _has_limiter = True
except ImportError:
    limiter = None  # type: ignore[assignment]
    _has_limiter = False
    logger.warning("slowapi not installed — rate limiting disabled")


# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup and auto-seed if hospitals table is empty."""
    try:
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables ready.")

        # Auto-seed hospitals if table is empty
        from database.connection import SessionLocal
        session = SessionLocal()
        try:
            hospital_count = session.query(models.Hospital).count()
            if hospital_count == 0:
                logger.info("Hospitals table empty — auto-seeding partner hospitals...")
                from database.seed import seed_hospitals
                seeded = seed_hospitals(session)
                logger.info(f"Auto-seeded {seeded} hospitals.")
        except Exception as e:
            logger.warning(f"Auto-seed skipped: {e}")

        # Auto-seed admin user if ADMIN_EMAIL is set and user doesn't exist
        try:
            admin_email = os.getenv("ADMIN_EMAIL")
            admin_password = os.getenv("ADMIN_PASSWORD")
            if admin_email and admin_password:
                existing = session.query(models.User).filter_by(email=admin_email).first()
                if not existing:
                    from auth import get_password_hash
                    admin_user = models.User(
                        email=admin_email,
                        hashed_password=get_password_hash(admin_password),
                        full_name="Admin",
                        role="admin",
                    )
                    session.add(admin_user)
                    session.commit()
                    logger.info(f"Admin user seeded: {admin_email}")
        except Exception as e:
            logger.warning(f"Admin seed skipped: {e}")
        finally:
            session.close()
    except Exception as e:
        logger.warning(f"Database init skipped: {e}")
    yield


app = FastAPI(
    title="AntiGravity ThaiTurk API",
    description="Medical · Travel · Factory · Marketing — AI-powered routing platform",
    version="2.0.0",
    lifespan=lifespan,
)

# Attach limiter
if _has_limiter:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# ---------------------------------------------------------------------------
# Global exception handler
# ---------------------------------------------------------------------------

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Catch unhandled exceptions and return structured error response."""
    logger.error(f"Unhandled exception on {request.method} {request.url.path}: {exc}")
    if not _is_production:
        logger.error(traceback.format_exc())

    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "An internal error occurred." if _is_production else str(exc),
                "details": None if _is_production else traceback.format_exc().split("\n")[-3:],
            }
        },
    )


# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

_origins = os.getenv("ALLOWED_ORIGINS", "")
if not _origins:
    if _is_production:
        logger.warning("ALLOWED_ORIGINS not set in production — defaulting to known domains")
        _origin_list = [
            "https://leblepito.com",
            "https://www.leblepito.com",
        ]
        _railway_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN", "")
        if _railway_domain:
            _origin_list.append(f"https://{_railway_domain}")
    else:
        _origin_list = ["http://localhost:3000", "http://127.0.0.1:3000"]
else:
    _origin_list = [o.strip() for o in _origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=_origin_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

orchestrator = AgentRouter()

# Register routers
app.include_router(auth_router)
app.include_router(medical_router)
app.include_router(travel_router)
app.include_router(marketing_router)
app.include_router(chat_router)
app.include_router(blog_router)
app.include_router(meshy_router)
app.include_router(notification_router)


class InboundRequest(BaseModel):
    message: str
    language: str | None = None
    metadata: dict | None = None


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "version": "2.0.0", "environment": _env}


@app.post("/api/classify")
def classify(req: InboundRequest) -> dict:
    """Gelen talebi sınıflandır ve ilgili agent'a yönlendir."""
    return orchestrator.route({"message": req.message, "language": req.language})


@app.post("/api/admin/seed")
def run_seed(_admin=Depends(require_admin)) -> dict:
    """One-time DB seeder — requires admin JWT."""
    from database.seed import seed_hospitals, seed_demo_patients
    from database.connection import SessionLocal
    session = SessionLocal()
    try:
        h = seed_hospitals(session)
        p = seed_demo_patients(session)
        return {"hospitals_seeded": h, "patients_seeded": p}
    finally:
        session.close()


@app.get("/api/sectors")
def sectors() -> dict:
    return {
        "sectors": ["Medical", "Travel", "Factory", "Marketing"],
        "active": ["Medical", "Travel", "Marketing"],
        "dormant": ["Factory"],
    }
