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
│   ├── app/              # App Router pages
│   │   ├── page.tsx      # Landing page
│   │   ├── layout.tsx    # Root layout (fonts, providers)
│   │   ├── medical/
│   │   │   ├── page.tsx      # Medical intake form
│   │   │   ├── gallery/page.tsx  # Before/after case gallery (6 categories)
│   │   │   └── visualize/page.tsx # Meshy.ai visualization wizard
│   │   ├── blog/page.tsx     # Blog listing
│   │   └── error.tsx, loading.tsx, not-found.tsx
│   ├── components/       # Reusable UI components
│   │   ├── Navbar.tsx        # Top navigation (all pages)
│   │   ├── ChatWidget.tsx    # Floating AI chat widget
│   │   ├── MedBot.tsx        # Medical assistant chatbot (Dr. Leila — FAQ + Claude API fallback)
│   │   ├── BlogCard.tsx      # Blog post card
│   │   └── ...
│   ├── lib/              # Shared utilities
│   │   ├── api.ts            # API client helpers
│   │   ├── i18n.ts           # Translation dictionary (6 languages, 370+ keys)
│   │   └── LanguageContext.tsx # Language provider & useLanguage() hook
│   ├── Dockerfile        # Node 20 alpine container
│   ├── package.json      # Node dependencies
│   ├── next.config.ts    # API proxy rewrites to backend
│   ├── railway.json      # Railway deployment config (standalone output)
│   └── nixpacks.toml     # Nixpacks build: Node 22, standalone output
│
├── 02_backend/           # FastAPI (Python 3.11)
│   ├── main.py           # App entrypoint — lifespan, CORS, rate limiting, 8 routers
│   ├── auth.py           # JWT token creation/validation, password hashing (bcrypt)
│   ├── routers/          # API route modules (8 routers)
│   │   ├── auth.py       # /api/auth/* — login, register, password, JWT
│   │   ├── medical.py    # /api/medical/* — intake, patients, hospitals, commissions
│   │   ├── travel.py     # /api/travel/* — travel options, destinations
│   │   ├── chat.py       # /api/chat/* — Claude-powered AI chatbot sessions
│   │   ├── marketing.py  # /api/marketing/* — SEO, content, campaigns, leads, publishing
│   │   ├── blog.py       # /api/blog/* — blog posts, categories, featured
│   │   ├── meshy.py      # /api/meshy/* — before/after AI visualization (Meshy.ai)
│   │   └── notification.py # /api/notifications/* — WhatsApp, Telegram, LINE webhooks
│   ├── database/
│   │   ├── connection.py # SQLAlchemy 2.0 engine, SessionLocal, get_db dependency
│   │   ├── models.py     # 11 ORM models (User, Hospital, Patient, ChatSession, etc.)
│   │   └── seed.py       # Auto-seed partner hospitals & demo data
│   ├── models/           # Pydantic request/response schemas
│   │   ├── medical.py    # Medical intake schemas
│   │   └── marketing.py  # Marketing endpoint schemas (SEO, campaign, lead, publish)
│   ├── alembic/          # Database migrations (Alembic)
│   ├── alembic.ini       # Alembic config
│   ├── Dockerfile        # Python 3.12 slim container
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
│   │   ├── notification.py     # Multi-channel notifications (WhatsApp, Telegram, LINE)
│   │   ├── calendar_sync.py    # Calendar integration (planned)
│   │   ├── region_profiles.py  # Region-specific marketing profiles
│   │   ├── blog_seed_data.py   # Static blog content (multi-language)
│   │   └── seo_content_engine.py # Extended SEO content engine
│   ├── memory/                 # Agent memory/context storage (placeholder)
│   └── logs/                   # AGENT_SESSION.log (auto-created, gitignored)
│
├── Makefile              # Dev targets: make dev, install, build, lint, typecheck, docker-up/down
├── docker-compose.yml    # Full-stack: PostgreSQL 16 + backend + frontend
├── dev.sh                # Quick-start script (backend + frontend in parallel)
├── .env.example          # Root environment template (all services)
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
- **Authentication:** JWT via python-jose + bcrypt password hashing via passlib
- **AI SDK:** anthropic (Claude API) for chat agent
- **Rate limiting:** slowapi (optional, graceful fallback)
- **HTTP client:** httpx (for internal API calls from chat agent)
- **Env management:** python-dotenv

### AI System (04_ai_agents)
- **Classification:** Rule-based keyword matching (55 medical, 65 travel, 54 factory, 251 marketing keywords)
- **Languages detected:** Turkish, English, Russian (Cyrillic)
- **Confidence scoring:** Normalized keyword hit ratio (0.0 - 1.0)
- **Chat agent:** Claude Sonnet (claude-sonnet-4-20250514) with tool-use (search_hospitals, get_procedure_pricing, submit_patient_inquiry, get_travel_quote)
- **Visualization:** Meshy.ai API for before/after medical procedure visualization
- **Notifications:** WhatsApp Business API, Telegram Bot API, LINE Messaging API

### Infrastructure
- **Hosting:** Railway (Nixpacks builder)
- **Database:** Railway PostgreSQL (DATABASE_URL env var, postgres:// auto-fixed to postgresql+psycopg2://)
- **Frontend deploy:** Node 22, standalone output, port from $PORT env
- **Backend deploy:** Python 3.11, uvicorn on $PORT
- **Health checks:** Backend `/health`, Frontend `/`
- **Containerization:** Docker Compose (local dev) with PostgreSQL 16, backend, frontend

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 20.9+
- PostgreSQL (local or Railway or Docker)

### Quick Start (Recommended)
```bash
# Option 1: Dev script
cp .env.example .env      # Fill in real values
./dev.sh                  # Starts backend (8000) + frontend (3000) in parallel

# Option 2: Makefile
make install              # Install all dependencies
make dev                  # Start both services

# Option 3: Docker
docker-compose up         # PostgreSQL + backend + frontend
```

### Manual Setup

#### Backend
```bash
cd 02_backend
cp .env.example .env          # Fill in real values
pip install -r requirements.txt
uvicorn main:app --reload     # Starts on http://localhost:8000
```

#### Frontend
```bash
cd 01_frontend
npm install
npm run dev                   # Starts on http://localhost:3000
```

### Makefile Targets
| Target | Description |
|--------|-------------|
| `make dev` | Start backend & frontend in parallel |
| `make dev-frontend` | Frontend only (port 3000) |
| `make dev-backend` | Backend only (port 8000) |
| `make install` | npm + pip install |
| `make build` | Next.js production build |
| `make typecheck` | TypeScript type checking |
| `make lint` | ESLint |
| `make docker-up` | Docker Compose up |
| `make docker-down` | Docker Compose down |
| `make health` | Test /health endpoint |
| `make clean` | Remove build artifacts |

### Key Environment Variables

#### Core
| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Production | PostgreSQL connection string |
| `ENVIRONMENT` | Optional | `development` (default) or `production` |
| `ALLOWED_ORIGINS` | Optional | CORS origins (comma-separated) |

#### AI Services
| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Production | Claude API key (chat agent) |
| `MESHY_API_KEY` | Production | Meshy.ai API key (visualization) |

#### Authentication
| Variable | Required | Description |
|----------|----------|-------------|
| `API_SECRET_KEY` | Production | JWT signing secret (HS256) |
| `ADMIN_EMAIL` | Production | Admin account email (auto-seeded on startup) |
| `ADMIN_PASSWORD` | Production | Admin account password (auto-seeded on startup) |

#### Notification Channels
| Variable | Required | Description |
|----------|----------|-------------|
| `WHATSAPP_TOKEN` | Optional | WhatsApp Business API token |
| `WHATSAPP_PHONE_ID` | Optional | WhatsApp phone number ID |
| `COORDINATOR_WHATSAPP` | Optional | Coordinator WhatsApp number |
| `TELEGRAM_BOT_TOKEN` | Optional | Telegram bot token |
| `TELEGRAM_COORDINATOR_CHAT_ID` | Optional | Telegram coordinator chat ID |
| `LINE_CHANNEL_ACCESS_TOKEN` | Optional | LINE channel access token |
| `LINE_CHANNEL_SECRET` | Optional | LINE channel secret (webhook verification) |

#### Frontend
| Variable | Required | Description |
|----------|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Frontend | Backend URL for API proxy (default: http://localhost:8000) |
| `NEXT_PUBLIC_SITE_URL` | Frontend | Site canonical URL (default: https://leblepito.com) |

## Authentication & Authorization

### JWT System (`02_backend/auth.py`)
- **Algorithm:** HS256 with `API_SECRET_KEY`
- **Token expiry:** 24 hours
- **Payload:** `{"sub": email, "role": role, "exp": expiration}`
- **Password hashing:** bcrypt via passlib

### Roles
| Role | Access |
|------|--------|
| `admin` | Full access — user management, notifications, seed data |
| `staff` | Standard operations — patient management, content |
| `coordinator` | Medical coordination — patient intake, travel |

### FastAPI Dependencies
- `get_current_user()` — Extracts user from JWT Bearer token
- `require_admin()` — Restricts endpoint to admin role only

### Admin Auto-Seeding
On startup, if `ADMIN_EMAIL` and `ADMIN_PASSWORD` env vars are set and no admin user exists, an admin account is automatically created.

## Notification System

### Multi-Channel Architecture (`04_ai_agents/skills/notification.py`)

Unified `NotificationService` class supporting 3 messaging channels:

| Channel | API | Use Case |
|---------|-----|----------|
| WhatsApp Business | Meta Cloud API | Turkish, English, Arabic patients |
| Telegram Bot | Telegram Bot API | Russian patients, coordinator alerts |
| LINE Messaging | LINE Messaging API | Thai, Chinese patients |

### Region-Aware Routing
```
Turkish/English → WhatsApp
Russian         → Telegram
Thai/Chinese    → LINE
Arabic          → WhatsApp
```

### Integration Flow
1. Patient submits intake form
2. Medical agent processes intake
3. `notify_coordinator()` — Alerts coordinator via Telegram + region channel
4. `notify_patient()` — Sends confirmation via patient's preferred channel
5. Graceful degradation if notification config is missing

### Webhook Handlers
- `POST /api/notifications/webhook/whatsapp` — WhatsApp incoming messages
- `POST /api/notifications/webhook/telegram` — Telegram updates
- `POST /api/notifications/webhook/line` — LINE events (with signature verification)

## API Architecture

### Sector Routing
All incoming requests can be classified via `POST /api/classify` which routes to:
- **Auth** (`/api/auth/*`) — JWT authentication and user management
- **Medical** (`/api/medical/*`) — Patient intake, hospital matching, commission tracking
- **Travel** (`/api/travel/*`) — Hotel/restaurant booking coordination
- **Marketing** (`/api/marketing/*`) — SEO, content generation, campaigns, analytics
- **Chat** (`/api/chat/*`) — AI-powered conversational medical secretary
- **Blog** (`/api/blog/*`) — Multi-language blog content
- **Meshy** (`/api/meshy/*`) — AI visualization (before/after)
- **Notifications** (`/api/notifications/*`) — Multi-channel messaging

### API Endpoints

#### System
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | — | Health check (version, environment) |
| POST | `/api/classify` | — | Master classifier — routes to sector agent |
| GET | `/api/sectors` | — | List available sectors |

#### Authentication (`/api/auth`)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/auth/login` | — | Email + password → JWT token |
| POST | `/api/auth/register` | Admin | Create new user account |
| GET | `/api/auth/me` | JWT | Get current user info |
| PATCH | `/api/auth/password` | JWT | Change password |

#### Medical (`/api/medical`)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/medical/intake` | — | Submit patient intake form |
| GET | `/api/medical/patient/{patient_id}` | — | Get patient by ID |
| GET | `/api/medical/patients` | — | List all patients |
| GET | `/api/medical/hospitals` | — | List partner hospitals |
| GET | `/api/medical/procedures` | — | Procedure categories & pricing |
| GET | `/api/medical/commission/summary` | — | Commission pipeline overview |
| PATCH | `/api/medical/patient/status` | JWT | Update patient status |

#### Travel (`/api/travel`)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/travel/options` | — | Submit travel request, get suggestions |
| GET | `/api/travel/destinations` | — | List travel destinations |

#### Chat (`/api/chat`)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/chat/session` | — | Start AI chat session |
| POST | `/api/chat/message` | — | Send message, get AI response |
| GET | `/api/chat/history/{session_id}` | — | Get chat history |

#### Marketing (`/api/marketing`)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/marketing/seo/analyze` | — | SEO keyword analysis |
| POST | `/api/marketing/seo/meta` | — | Generate meta tags |
| POST | `/api/marketing/content/blog` | — | Generate blog content |
| POST | `/api/marketing/content/ad-copy` | — | Generate ad copy |
| POST | `/api/marketing/content/social` | — | Generate social media content |
| POST | `/api/marketing/campaign/plan` | — | Create marketing campaign |
| POST | `/api/marketing/campaign/budget` | — | Budget allocation |
| GET | `/api/marketing/campaign/roi` | — | ROI estimation |
| POST | `/api/marketing/analytics/report` | — | Performance report |
| GET | `/api/marketing/analytics/funnel` | — | Funnel metrics |
| POST | `/api/marketing/leads/segment` | — | Lead segmentation |
| POST | `/api/marketing/leads/score` | — | Lead scoring |
| POST | `/api/marketing/publish/schedule` | — | Schedule content |
| POST | `/api/marketing/publish/now` | — | Publish immediately |
| GET | `/api/marketing/publish/queue` | — | View publish queue |
| GET | `/api/marketing/regions` | — | Available regions |
| GET | `/api/marketing/platforms` | — | Available platforms |

#### Blog (`/api/blog`)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/blog/posts` | — | List posts (paginated, filterable) |
| GET | `/api/blog/posts/{slug}` | — | Get post by slug |
| GET | `/api/blog/categories` | — | List categories |
| GET | `/api/blog/featured` | — | Featured posts |
| GET | `/api/blog/slugs` | — | All slugs (for SSG) |
| POST | `/api/blog/generate` | Admin | Generate blog content |

#### Meshy Visualization (`/api/meshy`)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/meshy/questions` | — | Get procedure questions |
| POST | `/api/meshy/visualize` | — | Start AI visualization job |
| GET | `/api/meshy/status/{viz_id}` | — | Check visualization status |
| POST | `/api/meshy/post-op` | — | Post-op comparison |

#### Notifications (`/api/notifications`)
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/notifications/channels` | — | List active channels & config status |
| POST | `/api/notifications/send` | Admin | Send notification to channel |
| POST | `/api/notifications/test` | Admin | Test notification delivery |
| POST | `/api/notifications/webhook/whatsapp` | — | WhatsApp incoming webhook |
| POST | `/api/notifications/webhook/telegram` | — | Telegram incoming webhook |
| POST | `/api/notifications/webhook/line` | — | LINE incoming webhook |

#### Admin
| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/admin/seed` | Admin | Seed demo data |

## Database Schema (PostgreSQL, 11 tables)

1. **users** — Authentication accounts (email, hashed_password, role: admin/staff/coordinator)
2. **hospitals** — Partner hospital registry (Turkey + Thailand)
3. **patients** — Medical patient intake records with hospital matching, commission & status
4. **travel_requests** — Travel/hotel booking requests
5. **campaigns** — Marketing campaign plans with budget splits & ROI
6. **leads** — Marketing leads with scoring & segmentation
7. **publish_queue** — Scheduled content for auto-publishing
8. **conversions** — Marketing conversion tracking
9. **chat_sessions** — AI chatbot session metadata
10. **chat_messages** — Chat message history (user + assistant)
11. **visualizations** — Meshy.ai before/after visualization records

Auto-seeding: On startup, if `hospitals` table is empty, partner hospitals are auto-seeded via `database/seed.py`. If `ADMIN_EMAIL`/`ADMIN_PASSWORD` are set, admin user is auto-created.

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

### MedBot (Frontend Chat — `01_frontend/components/MedBot.tsx`)
- Floating medical assistant named "Dr. Leila"
- **FAQ mode:** Keyword-matched responses for common questions (pricing, hospitals, procedures)
- **AI fallback:** Routes unmatched queries to `/api/chat/message` (Claude API)
- Quick action buttons on first interaction
- Escalation to human coordinator after 2 exchanges
- RTL support for Arabic, markdown rendering, auto-scroll
- Responsive: card on desktop, full-screen on mobile

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
- Component files: PascalCase (`BlogCard.tsx`, `ChatWidget.tsx`, `MedBot.tsx`)

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

### Docker (Local Development)
- `docker-compose.yml` with 3 services: PostgreSQL 16, FastAPI backend, Next.js frontend
- PostgreSQL 16 with persistent volume, healthcheck via `pg_isready`
- Backend mounts `./02_backend:/app` for hot-reload
- Frontend connects to backend via Docker network

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
- MedBot frontend chatbot (FAQ + AI fallback)
- Meshy.ai visualization integration
- Medical gallery (before/after case studies, 6 categories)
- Blog system (multi-language seed data)
- Multi-language routing (6 languages, 370+ i18n keys)
- JWT authentication (admin/staff/coordinator roles)
- Multi-channel notifications (WhatsApp, Telegram, LINE)
- FastAPI backend with PostgreSQL (11 tables)
- Next.js frontend with medical intake form
- Railway deployment configs
- Docker Compose + Makefile + dev scripts

### Planned / In Progress
- [ ] Firebase/Firestore integration (legacy, mostly replaced by PostgreSQL)
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
7. **Frontend API proxy** — Frontend never calls backend directly. All API calls go through `/api/*` which Next.js rewrites to `NEXT_PUBLIC_API_URL`.
8. **Commission rates are internal** — Chat agent system prompt explicitly says never reveal commission rates to users.
9. **Rate limiting** — Medical intake: 10/min per IP, Chat messages: 20/min per IP, Meshy visualization: 1/day per IP, 20/day global.
10. **Blog content is static** — `blog_seed_data.py` contains hardcoded multi-language blog posts. No dynamic generation yet.
11. **Auth is JWT-based** — Protected endpoints use `require_admin()` or `get_current_user()` FastAPI dependencies. Admin auto-seeded on startup.
12. **Notifications are fire-and-forget** — Channel config is optional; missing tokens disable that channel silently.
13. **MedBot vs ChatWidget** — MedBot (Dr. Leila) is the newer FAQ-first assistant; ChatWidget is the older full-API chat. MedBot is used in medical pages.
