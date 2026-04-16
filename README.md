# 🏥 Golden Hour

> **Health Early Warning System** — Offline-first clinical decision support for frontline health workers.

[![CI](https://github.com/Andreamercy/golden-hour/actions/workflows/ci.yml/badge.svg)](https://github.com/Andreamercy/golden-hour/actions)

---

## What it does

Golden Hour helps community health workers and nurses detect patient deterioration early using the **NEWS2** (National Early Warning Score 2) and **MEOWS** (Modified Early Obstetric Warning Score) clinical scoring systems.

- 📱 **Mobile app** (React Native / Expo) — works fully offline
- 🖥️ **Supervisor dashboard** (Next.js) — real-time alerts and geographic map
- ⚙️ **Backend API** (FastAPI + PostgreSQL + Redis)
- 📊 **Scoring engine** — deterministic NEWS2 / MEOWS, no LLM at point-of-care
- 🚨 **Alert system** — SMS fallback + push notifications + escalation chain

---

## Monorepo structure

```
golden-hour/
├── packages/
│   ├── shared/        TypeScript types, NEWS2/MEOWS scoring, Zod validation
│   ├── mobile/        React Native (Expo) app — Android 9+
│   ├── api/           FastAPI backend
│   └── dashboard/     Next.js 14 supervisor dashboard
├── scripts/           Seed, mock-data, deploy, backup scripts
├── docker-compose.yml Dev environment (PostgreSQL 16 + Redis 7)
└── BUILD_GUIDE.md     Step-by-step build prompts
```

---

## Quick start

```bash
# Prerequisites: Node 20+, pnpm 9+, Python 3.11+, Docker
make setup       # install all deps
make dev         # start PostgreSQL + Redis + API + dashboard
```

---

## Critical rules

1. **NEWS2 scoring is sacred** — every threshold matches the Royal College of Physicians spec exactly.
2. **Offline-first** — the mobile app works with zero connectivity.
3. **No LLM at point of care** — all action cards are pre-authored from WHO/NHS guidelines.
4. **Every alert matters** — HIGH/CRITICAL alerts are queued with retry until delivered.
5. **Privacy by default** — raw patient vitals are never logged.

---

## Tech stack

| Layer | Tech |
|---|---|
| Mobile | React Native, Expo SDK 51+, expo-sqlite, expo-sms |
| Dashboard | Next.js 14, Tailwind CSS, Recharts, Leaflet |
| API | FastAPI, SQLAlchemy, Alembic, asyncpg |
| DB | PostgreSQL 16 + PostGIS |
| Cache / PubSub | Redis 7 + BullMQ |
| Shared logic | TypeScript strict, Zod, Vitest |
| CI/CD | GitHub Actions, Docker, Railway / Fly.io |

---

## Deployment targets

- **Railway** (recommended for demo)
- **Fly.io** (free tier alternative)
- **Self-hosted** — DigitalOcean $6/month droplet + Docker Compose

---

## License

MIT
