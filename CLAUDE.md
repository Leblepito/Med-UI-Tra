# CLAUDE.md — Med-UI-Tra (AntiGravity ThaiTurk Platform)

AI-powered multi-sector referral platform for medical tourism (Phuket-Turkey corridor), travel bookings, B2B manufacturing, and digital marketing.

## Project Overview

**Brand:** AntiGravity Ventures / AntiGravity Medical
**Domain:** leblepito.com
**Business model:** Commission-based medical tourism referrals (22-25%) + hotel operations + marketing services
**Supported languages:** Russian (ru), Turkish (tr), English (en), Thai (th), Arabic (ar), Chinese (zh)
**Business regions:** Turkey, Russia, UAE, Europe, Asia

## Repository Structure

```
Med-UI-Tra/
├── 01_frontend/          # Next.js 16 (React 19, TypeScript, TailwindCSS v4)
│   ├── app/              # App Router pages (page.tsx, layout.tsx, error/loading/not-found)
│   ├── components/       # Reusable UI components (Navbar, ChatWidget, BlogCard, etc.)
│   ├── lib/              # Shared utilities (api.ts, i18n.ts, LanguageContext.tsx)
│   ├── package.json      # Node dependencies
│   ├── next.config.ts    # API proxy rewrites to backend
│   ├── railway.json      # Railway deployment config (standalone output)
│   └── nixpacks.toml     # Nixpacks build: Node 22, standalone output
│
├── 02_backend/           # FastAPI (Python 3.11)
│   ├── main.py           # App entrypoint — lifespan, CORS, rate limiting, router registration
│   ├── routers/          # API route modules
│   │   ├── medical.py    # /api/medical/* — intake, patients, hospitals, commissions
│   │   ├── travel.py     # /api/travel/* — travel options, destinations
│   │   ├── chat.py       # /api/chat/* — Claude-powered AI chatbot sessions
│   │   ├── marketing.py  # /api/marketing/* — SEO, content, campaigns, leads, publishing
│   │   ├── blog.py       # /api/blog/* — blog posts, categories, featured
│   │   └── meshy.py      # /api/meshy/* — before/after AI visualization (Meshy.ai)
│   ├── database/
│   │   ├── connection.py # SQLAlchemy 2.0 engine, SessionLocal, get_db dependency
│   │   ├── models.py     # 10 ORM models (Hospital, Patient, TravelRequest, Campaign, Lead, etc.)
│   │   └── seed.py       # Auto-seed partner hospitals & demo data
│   ├── models/           # Pydantic request/response schemas
│   │   ├── medical.py    # Medical intake schemas
│   │   └── marketing.py  # Marketing endpoint schemas (SEO, campaign, lead, publish)
│   ├── alembic/          # Database migrations (Alembic)
│   ├── alembic.ini       # Alembic config
│   ├── requirements.txt  # Python dependencies
│   ├── railway.json      # Railway deployment config
│   ├── nixpacks.toml     # Nixpacks build: Python 3.11 + gcc
│   └── .env.example      # Environment variable template
│
├── 03_data/              # Data layer
│   ├── firebase/         # Legacy Firestore schema docs (replaced by PostgreSQL)
│   │   └── schema.md     # Collection schemas for patients, hospitals, travel_requests
│   ├── migrations/       # Placeholder for migration scripts
│   └── seeds/
│       └── demo_data.py  # Demo data seeder
│
├── 04_ai_agents/         # AI Agent System
│   ├── master_orchestrator.py  # Request classifier & agent router (keyword-based, TR/EN/RU)
│   ├── agents/
│   │   ├── medical_agent.py    # Patient intake, hospital matching, commission calculation
│   │   ├── travel_agent.py     # Hotel pricing, availability, reservation coordination
│   │   ├── chat_agent.py       # Claude API chatbot with tool-use (search_hospitals, pricing, intake)
│   │   ├── marketing_agent.py  # SEO, content, campaigns, analytics, lead funnel, publishing
│   │   ├── factory_agent.py    # B2B textile/manufacturing (dormant)
│   │   └── meshy_agent.py      # Meshy.ai before/after visualization integration
│   ├── skills/                 # Modular skill modules used by agents
│   │   ├── seo_engine.py       # Keyword analysis, meta tag generation, SEO scoring
│   │   ├── content_generator.py # Blog, ad copy, social media, landing page, email generation
│   │   ├── campaign_manager.py # Campaign planning, budget split, ROI estimation
│   │   ├── analytics_tracker.py # Performance reports, funnel metrics
│   │   ├── lead_funnel.py      # Lead segmentation & scoring
│   │   ├── auto_publisher.py   # Scheduled/instant content publishing
│   │   ├── commission.py       # Commission calculation utilities
│   │   ├── translation.py      # Multi-language translation support
│   │   ├── calendar_sync.py    # Calendar integration (planned)
│   │   ├── region_profiles.py  # Region-specific marketing profiles
│   │   ├── blog_seed_data.py   # Static blog content (multi-language)
│   │   └── seo_content_engine.py # Extended SEO content engine
│   ├── memory/                 # Agent memory/context storage (placeholder)
│   └── logs/                   # AGENT_SESSION.log (auto-created, gitignored)
│
├── README.md             # Project overview
├── railway.json          # Root Railway config (backend deploy)
├── requirements.txt      # Root Python deps (mirrors 02_backend)
└── .gitignore            # Python, Node, env, IDE, logs
```

## Tech Stack

### Frontend (01_frontend)
- **Framework:** Next.js 16.1 with App Router
- **React:** 19.2 with Server Components and Client Components
- **Language:** TypeScript 5.9 (strict mode)
- **Styling:** TailwindCSS v4 with PostCSS
- **Fonts:** Lora (serif display), Manrope (body), Noto Sans Thai/Arabic/Chinese
- **i18n:** Custom `LanguageContext` + `i18n.ts` dictionary (6 languages: ru, tr, en, th, ar, zh)
- **API layer:** Proxy rewrites in `next.config.ts` — all `/api/*` routes forward to FastAPI backend
- **Output:** Standalone mode for Railway deployment

### Backend (02_backend)
- **Framework:** FastAPI 0.115+ with Pydantic v2
- **Server:** uvicorn with standard extras
- **Database:** PostgreSQL via SQLAlchemy 2.0 + psycopg2-binary
- **Migrations:** Alembic
- **AI SDK:** anthropic (Claude API) for chat agent
- **Rate limiting:** slowapi (optional, graceful fallback)
- **HTTP client:** httpx (for internal API calls from chat agent)
- **Env management:** python-dotenv

### AI System (04_ai_agents)
- **Classification:** Rule-based keyword matching (91 medical, 63 travel, 50 factory, ~50 marketing keywords)
- **Languages detected:** Turkish, English, Russian (Cyrillic)
- **Confidence scoring:** Normalized keyword hit ratio (0.0 - 1.0)
- **Chat agent:** Claude Sonnet (claude-sonnet-4-20250514) with tool-use (search_hospitals, get_procedure_pricing, submit_patient_inquiry, get_travel_quote)
- **Visualization:** Meshy.ai API for before/after medical procedure visualization

### Infrastructure
- **Hosting:** Railway (Nixpacks builder)
- **Database:** Railway PostgreSQL (DATABASE_URL env var, postgres:// auto-fixed to postgresql+psycopg2://)
- **Frontend deploy:** Node 22, standalone output, port from $PORT env
- **Backend deploy:** Python 3.11, uvicorn on $PORT
- **Health checks:** Backend `/health`, Frontend `/`

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 20.9+
- PostgreSQL (local or Railway)

### Backend
```bash
cd 02_backend
cp .env.example .env          # Fill in real values
pip install -r requirements.txt
uvicorn main:app --reload     # Starts on http://localhost:8000
```

### Frontend
```bash
cd 01_frontend
npm install
npm run dev                   # Starts on http://localhost:3000
```

### Key environment variables
| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Production | PostgreSQL connection string |
| `ANTHROPIC_API_KEY` | Production | Claude API key (chat agent) |
| `MESHY_API_KEY` | Production | Meshy.ai API key (visualization) |
| `ENVIRONMENT` | Optional | `development` (default) or `production` |
| `ALLOWED_ORIGINS` | Optional | CORS origins (comma-separated) |
| `ADMIN_SECRET` | Production | Secret for admin seed endpoint |
| `BACKEND_URL` | Frontend | Backend URL for API proxy (default: http://localhost:8000) |

## API Architecture

### Sector Routing
All incoming requests can be classified via `POST /api/classify` which routes to:
- **Medical** (`/api/medical/*`) — Patient intake, hospital matching, commission tracking
- **Travel** (`/api/travel/*`) — Hotel/restaurant booking coordination
- **Marketing** (`/api/marketing/*`) — SEO, content generation, campaigns, analytics
- **Chat** (`/api/chat/*`) — AI-powered conversational medical secretary
- **Blog** (`/api/blog/*`) — Multi-language blog content
- **Meshy** (`/api/meshy/*`) — AI visualization (before/after)

### Key API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check (version, environment) |
| POST | `/api/classify` | Master classifier — routes to sector agent |
| POST | `/api/medical/intake` | Submit patient intake form |
| GET | `/api/medical/hospitals` | List partner hospitals |
| GET | `/api/medical/procedures` | Procedure categories & pricing |
| GET | `/api/medical/commission/summary` | Commission pipeline overview |
| POST | `/api/travel/options` | Submit travel request, get suggestions |
| POST | `/api/chat/session` | Start AI chat session |
| POST | `/api/chat/message` | Send message, get AI response |
| POST | `/api/marketing/seo/analyze` | SEO keyword analysis |
| POST | `/api/marketing/campaign/plan` | Create marketing campaign |
| POST | `/api/meshy/visualize` | Start AI visualization job |
| GET | `/api/blog/posts` | List blog posts (paginated, filterable) |

## Database Schema (PostgreSQL, 10 tables)

1. **hospitals** — Partner hospital registry (Turkey + Thailand)
2. **patients** — Medical patient intake records with hospital matching & commission
3. **travel_requests** — Travel/hotel booking requests
4. **campaigns** — Marketing campaign plans with budget splits & ROI
5. **leads** — Marketing leads with scoring & segmentation
6. **publish_queue** — Scheduled content for auto-publishing
7. **conversions** — Marketing conversion tracking
8. **chat_sessions** — AI chatbot session metadata
9. **chat_messages** — Chat message history (user + assistant)
10. **visualizations** — Meshy.ai before/after visualization records

Auto-seeding: On startup, if `hospitals` table is empty, partner hospitals are auto-seeded via `database/seed.py`.

## Agent System Architecture

### Master Orchestrator (`04_ai_agents/master_orchestrator.py`)
- `RequestClassifier` — Regex-based keyword matching across 4 sectors
- `AgentRouter` — Routes classified requests to the appropriate agent
- Supports CLI mode for interactive testing (`python master_orchestrator.py`)

### Agent Pattern
Each agent follows this pattern:
- Lazy initialization with graceful fallback if dependencies unavailable
- `handle(request: dict)` or `process_intake(data: dict, db=None)` entry point
- DB parameter is optional — agents work with in-memory fallback when `db=None`
- Structured dict responses with `status`, `action`, and domain-specific data

### Chat Agent (Claude API Integration)
- Model: `claude-sonnet-4-20250514`
- Max tokens: 1024, max tool rounds: 3
- 4 tools: `search_hospitals`, `get_procedure_pricing`, `submit_patient_inquiry`, `get_travel_quote`
- System prompt includes full business data (hospitals, pricing, patient journey)
- DB-backed tool execution (falls back to static data if DB unavailable)
- Multilingual greetings and fallback responses (6 languages)

## Code Conventions

### Python (Backend + AI Agents)
- Python 3.11+ with `from __future__ import annotations`
- Type hints throughout (PEP 484 style)
- Pydantic v2 models for request/response validation
- SQLAlchemy 2.0 ORM with DeclarativeBase
- `snake_case` for variables, functions, files
- `PascalCase` for classes
- Comments in Turkish and English (mixed, business domain in Turkish)
- Logger names: `thaiturk.*` for backend, agent names for AI modules
- Graceful import fallbacks with try/except for optional dependencies (slowapi, anthropic)
- DB dependency injection via FastAPI `Depends(get_db)` or agent `db=None` parameter

### TypeScript (Frontend)
- Strict TypeScript with Next.js App Router
- `"use client"` directive for interactive components
- Path aliases: `@/*` maps to project root
- API calls through `/api/*` proxy (never direct backend URLs)
- i18n via `useLanguage()` hook from `LanguageContext`
- TailwindCSS utility classes, no separate CSS modules
- Component files: PascalCase (`BlogCard.tsx`, `ChatWidget.tsx`)

### Naming Conventions
- Patient IDs: `MED-YYYYMMDD-XXXXXX`
- Travel request IDs: `TRV-YYYYMMDD-XXXXXX`
- Campaign IDs: `CMP-XXXXXXXX`
- Visualization IDs: `VIZ-YYYYMMDD-XXXXXX`
- Chat session IDs: `chat-{hex12}`
- Chat message IDs: `msg-{hex10}`

## Deployment (Railway)

### Services
1. **Backend** — Root `railway.json` deploys `02_backend/main.py` via `uvicorn`
2. **Frontend** — `01_frontend/railway.json` deploys Next.js standalone server

### Build System
- **Nixpacks** builder for both services
- Backend: Python 3.11 + gcc (for psycopg2 compilation)
- Frontend: Node 22 + npm, `next build` → standalone output with static assets copied

### Health Checks
- Backend: `GET /health` (30s timeout)
- Frontend: `GET /` (60s timeout)
- Restart policy: ON_FAILURE with 3-5 retries

### CORS Configuration
- Production: `https://leblepito.com`, `https://www.leblepito.com`, Railway public domain
- Development: `http://localhost:3000`, `http://127.0.0.1:3000`

## Project Status & Roadmap

### Completed
- AI classification engine (4 sectors, multilingual keyword matching)
- Medical agent (full pipeline: intake → hospital matching → commission)
- Travel agent (pricing, availability, coordinator messages)
- Marketing agent (SEO, content, campaigns, analytics, leads, publishing)
- Chat agent (Claude API with tool-use)
- Meshy.ai visualization integration
- Blog system (multi-language seed data)
- Multi-language routing (6 languages)
- FastAPI backend with PostgreSQL
- Next.js frontend with medical intake form
- Railway deployment configs

### Planned / In Progress
- [ ] Firebase/Firestore integration (legacy, mostly replaced by PostgreSQL)
- [ ] Authentication system
- [ ] Travel & Factory UI pages
- [ ] Calendar MCP integration
- [ ] Real OTA channel sync (Booking.com, Airbnb)
- [ ] Factory agent activation (currently dormant)
- [ ] Real Meshy.ai image comparison (currently placeholder similarity score)

## Important Notes for AI Assistants

1. **Do NOT modify u2Algo project** — only work within this Med-UI-Tra repository
2. **sys.path manipulation** — Backend and agents use `sys.path.insert()` to cross-import between `02_backend/` and `04_ai_agents/`. This is by design.
3. **Graceful fallbacks** — All agents and routers have try/except import blocks. If a dependency is missing, they fall back to stubs or in-memory alternatives.
4. **Database is optional in dev** — Agents accept `db=None` and work with in-memory dictionaries. The backend auto-creates tables on startup.
5. **Railway postgres:// fix** — `database/connection.py` auto-replaces `postgres://` with `postgresql+psycopg2://` for Railway compatibility.
6. **Two requirements.txt files** — Root `requirements.txt` mirrors `02_backend/requirements.txt`. Keep them in sync.
7. **Frontend API proxy** — Frontend never calls backend directly. All API calls go through `/api/*` which Next.js rewrites to `BACKEND_URL`.
8. **Commission rates are internal** — Chat agent system prompt explicitly says never reveal commission rates to users.
9. **Rate limiting** — Medical intake: 10/min per IP, Chat messages: 20/min per IP, Meshy visualization: 1/day per IP, 20/day global.
10. **Blog content is static** — `blog_seed_data.py` contains hardcoded multi-language blog posts. No dynamic generation yet.
