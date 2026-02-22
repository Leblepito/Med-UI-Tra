# AntiGravity Ventures — ThaiTurk

AI-powered medical tourism platform connecting patients with top clinics across **Phuket** and **Turkey**. Multi-language, multi-channel, full-stack.

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│  01_frontend (Next.js 16 + React 19 + Tailwind v4)      │
│  ─ Multi-language UI ─ Blog ─ Gallery ─ MedBot Chat      │
│  ─ Meshy.ai Before/After Visualization                   │
└──────────────────┬───────────────────────────────────────┘
                   │  /api/* rewrite (next.config.ts)
┌──────────────────▼───────────────────────────────────────┐
│  02_backend (FastAPI + SQLAlchemy + PostgreSQL)           │
│  ─ 7 routers ─ JWT Auth ─ Rate Limiting                  │
│  ─ WhatsApp / Telegram / LINE notifications              │
└──────────┬───────────────────┬───────────────────────────┘
           │                   │
┌──────────▼──────┐  ┌────────▼──────────────────────────┐
│  PostgreSQL DB  │  │  04_ai_agents                      │
│  11 tables      │  │  ─ Master Orchestrator             │
│                 │  │  ─ Medical / Travel / Marketing    │
│                 │  │  ─ Meshy.ai Agent                  │
│                 │  │  ─ 9 Skills (SEO, Content, etc.)   │
└─────────────────┘  └───────────────────────────────────┘
```

## Features

| Sector | Status | Description |
|--------|--------|-------------|
| **Medical** | Active | Patient intake → procedure classification → hospital matching → commission calc |
| **Travel** | Active | Hotel & restaurant bookings with seasonal pricing |
| **Marketing** | Active | SEO engine, content generator, campaign manager, lead funnel, auto-publisher |
| **Factory** | Dormant | B2B textile/manufacturing (Phase 4) |

**Additional Features:**
- Blog system — 10 seed posts × 6 languages, SEO-optimized with JsonLd
- AI Chat (MedBot) — Multi-language medical tourism assistant
- Meshy.ai Visualization — Before/after AI-generated procedure previews (8 procedures)
- Gallery — Clinic and procedure photo galleries
- Auth — JWT-based authentication with role-based access (admin, staff, coordinator)
- Notifications — WhatsApp, Telegram, LINE messaging (region-aware channel selection)

## Languages

| Code | Language | Primary Regions |
|------|----------|-----------------|
| `tr` | Turkish | Turkey |
| `en` | English | Europe, Global |
| `ru` | Russian | Russia, CIS |
| `th` | Thai | Thailand, Asia |
| `ar` | Arabic | UAE, Middle East |
| `zh` | Chinese | China, East Asia |

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 16, React 19, TypeScript, Tailwind CSS v4 |
| Backend | FastAPI, Pydantic v2, SQLAlchemy 2.0, uvicorn |
| Database | PostgreSQL (Railway-compatible) |
| AI | Rule-based classification + Anthropic Claude + Meshy.ai |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Messaging | WhatsApp Business API, Telegram Bot API, LINE Messaging API |
| Deployment | Railway |

## Quick Start

### 1. Clone & configure

```bash
git clone https://github.com/Leblebito/Med-UI-Tra.git
cd Med-UI-Tra
cp .env.example .env
# Edit .env with your credentials
```

### 2. Backend

```bash
cd 02_backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 3. Frontend

```bash
cd 01_frontend
npm install
npm run dev
```

The frontend proxies `/api/*` requests to `localhost:8000` via `next.config.ts`.

### Environment Variables

```bash
# ── Core ──
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/thaiturk
ENVIRONMENT=development
ANTHROPIC_API_KEY=sk-ant-xxx
MESHY_API_KEY=your-meshy-api-key

# ── Auth ──
API_SECRET_KEY=your-jwt-secret-key
ADMIN_EMAIL=admin@thaiturk.com
ADMIN_PASSWORD=change-me-in-production

# ── Messaging ──
WHATSAPP_TOKEN=your-whatsapp-business-token
WHATSAPP_PHONE_ID=your-phone-number-id
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_COORDINATOR_CHAT_ID=your-chat-id
LINE_CHANNEL_ACCESS_TOKEN=your-line-channel-token
LINE_CHANNEL_SECRET=your-line-channel-secret

# ── Frontend ──
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API Endpoints (48 endpoints, 8 routers)

### Health & Core

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/health` | — | Health check |
| POST | `/api/classify` | — | AI request classification |
| POST | `/api/admin/seed` | JWT | Database seeder |
| GET | `/api/sectors` | — | Active sectors list |

### Auth (`/api/auth`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/auth/login` | — | Email + password → JWT token |
| POST | `/api/auth/register` | Admin | Create new user |
| GET | `/api/auth/me` | JWT | Current user info |
| PATCH | `/api/auth/password` | JWT | Change password |

### Medical (`/api/medical`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/medical/intake` | — | New patient intake |
| GET | `/api/medical/patient/{id}` | — | Get patient record |
| PATCH | `/api/medical/patient/status` | JWT | Update patient status |
| GET | `/api/medical/patients` | — | List patients |
| GET | `/api/medical/commission/summary` | — | Commission pipeline |
| GET | `/api/medical/hospitals` | — | Partner hospitals |
| GET | `/api/medical/procedures` | — | Procedures & pricing |

### Travel (`/api/travel`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/travel/booking` | — | New travel booking |
| GET | `/api/travel/destinations` | — | Available destinations |
| GET | `/api/travel/hotels` | — | Hotel listings |

### Marketing (`/api/marketing`)

17 endpoints covering SEO analysis, content generation, campaign management, analytics tracking, lead funnel, and auto-publishing.

### Blog (`/api/blog`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/blog/posts` | — | List posts (paginated) |
| GET | `/api/blog/posts/{slug}` | — | Get post by slug |
| GET | `/api/blog/categories` | — | List categories |
| GET | `/api/blog/featured` | — | Featured posts |
| GET | `/api/blog/slugs` | — | All slugs (for sitemap) |
| POST | `/api/blog/generate` | Admin | AI blog generation |

### Chat (`/api/chat`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/chat/session` | — | Create chat session |
| POST | `/api/chat/message` | — | Send message |
| GET | `/api/chat/session/{id}` | — | Get session history |

### Meshy Visualization (`/api/meshy`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/meshy/questions/{procedure}` | — | Get procedure questions |
| POST | `/api/meshy/generate` | — | Generate before/after |
| GET | `/api/meshy/status/{viz_id}` | — | Check generation status |
| GET | `/api/meshy/result/{viz_id}` | — | Get result images |

### Notifications (`/api/notifications`)

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/notifications/send` | Admin | Send manual notification |
| POST | `/api/notifications/test` | Admin | Test notification |
| GET | `/api/notifications/channels` | — | List active channels |
| POST | `/api/notifications/webhook/whatsapp` | — | WhatsApp incoming webhook |
| POST | `/api/notifications/webhook/telegram` | — | Telegram incoming webhook |
| POST | `/api/notifications/webhook/line` | — | LINE incoming webhook |

## Database Schema (11 tables)

`hospitals` · `patients` · `travel_requests` · `campaigns` · `leads` · `publish_queue` · `conversions` · `chat_sessions` · `chat_messages` · `visualizations` · `users`

## Partner Hospitals

- **Memorial Sisli** — Istanbul (aesthetic, bariatric, oncology)
- **Acibadem Maslak** — Istanbul (dental, checkup, ophthalmology, IVF)
- **EsteNove** — Antalya (aesthetic, hair, dermatology)
- **DentGroup** — Istanbul (dental)
- **HairCure** — Istanbul (hair transplant)

## AI Agent System

- **Master Orchestrator** — Multi-language request classification (TR/RU/EN/TH/AR/ZH) with confidence scoring
- **Medical Agent** — Patient intake → procedure classify → hospital match → commission calc → notification
- **Travel Agent** — Hotel/restaurant bookings with seasonal pricing
- **Marketing Agent** — SEO → content gen → campaign plan → analytics → lead funnel → auto publish
- **Meshy Agent** — Before/after AI visualization via Meshy.ai Image-to-Image API

### Skills (9)

`seo_engine` · `content_generator` · `campaign_manager` · `analytics_tracker` · `lead_funnel` · `auto_publisher` · `region_profiles` · `blog_seed_data` · `seo_content_engine` · `notification`

## Deployment (Railway)

The backend is configured for Railway deployment with:
- `DATABASE_URL` auto-injected by Railway PostgreSQL plugin
- `RAILWAY_PUBLIC_DOMAIN` for CORS configuration
- Health check at `/health`

## License

Proprietary — AntiGravity Ventures
