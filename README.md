# Med-UI-Tra

AI-powered multi-sector referral platform — medical tourism, travel bookings, and B2B manufacturing.

## Architecture

```
01_frontend/    → Next.js (React/TypeScript) — Multi-language intake forms
02_backend/     → FastAPI (Python) — REST API & business logic
03_data/        → Firebase/Firestore — Data layer (planned)
04_ai_agents/   → AI Agent System — Classification, routing & orchestration
```

## AI Agent System

- **Master Orchestrator** — Multi-language request classification (TR/RU/EN/TH) with confidence scoring
- **Medical Agent** — Patient intake, hospital matching (5 partner hospitals), commission tracking (22-25%)
- **Travel Agent** — Hotel/restaurant bookings with seasonal pricing
- **Factory Agent** — B2B textile/manufacturing (Phase 4, dormant)

### Supported Procedures
Rhinoplasty, hair transplant, dental implants, dermatology, full checkup, LASIK, gastric sleeve, IVF, oncology screening

## Quick Start

### Backend
```bash
cd 02_backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd 01_frontend
npm install
npm run dev
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/classify` | Request classification |
| POST | `/api/medical/intake` | Patient intake |
| GET | `/api/medical/hospitals` | Partner hospitals |
| GET | `/api/medical/procedures` | Procedure pricing |
| GET | `/api/medical/commission/summary` | Commission pipeline |

## Tech Stack

- **Frontend:** Next.js, React, TypeScript, TailwindCSS
- **Backend:** FastAPI, Pydantic, uvicorn
- **AI:** Rule-based classification with keyword matching (91 medical, 63 travel, 50 factory keywords)
- **Languages:** Russian, Turkish, English, Thai (detection)

## Project Status

- [x] AI classification engine
- [x] Medical agent (intake → hospital matching → commission)
- [x] Multi-language routing
- [x] FastAPI backend
- [x] Medical intake form (frontend)
- [ ] Database integration (Firestore)
- [ ] Authentication
- [ ] Travel & Factory UI pages
- [ ] Calendar MCP integration
