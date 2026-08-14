# Deploying MockBees to Vercel (and local Postgres setup)

This document explains how to deploy the `mockbees` project to Vercel (frontend + Python API) and how to run a local Postgres-based development stack using Docker Compose.

## 1) Vercel deployment (recommended for production frontend + serverless API)

Steps:

1. Push your repo to GitHub (or connect the repository to Vercel).
2. In Vercel, import the project and select the `main` branch.
3. Add Environment Variables in Vercel (Project Settings → Environment Variables):
   - `DATABASE_URL` — e.g. `postgres://user:pass@host:5432/dbname` (use a managed Postgres)
   - `SECRET_KEY` — a long random string
   - `GROQ_API_KEY` — required for AI question generation
   - `GOOGLE_CLIENT_ID` — optional
   - (optional) `VITE_API_URL` — leave unset to use same-origin `/api`

4. Vercel will build the frontend (uses `frontend/package.json`) and install Python dependencies from `api/requirements.txt` for the serverless API.
5. After deployment, the frontend will call the API at `/api` by default.

Notes:
- Do NOT use SQLite in production on Vercel — the filesystem is ephemeral. Use a managed Postgres and set `DATABASE_URL` accordingly.
- Make sure your `GROQ_API_KEY` account has sufficient quota for generation.

## 2) Local development with Docker Compose (Postgres + backend + frontend build)

Prerequisites: `docker` and `docker-compose` installed.

From repo root, copy `.env.example` to `.env` and edit values.

Commands:

```bash
docker compose up --build
```

This will start:
- `db` — Postgres database
- `backend` — Python FastAPI app served by `uvicorn` on port `8000`

Frontend local dev (optional):
- You can run the frontend locally with `npm install` and `npm run dev` from `frontend/` and point `VITE_API_URL` at `http://localhost:8000/api`.

## 3) Environment variables (example keys)

- `DATABASE_URL=postgresql://postgres:postgres@db:5432/mockbees`
- `SECRET_KEY=supersecretchangeme`
- `GROQ_API_KEY=your_groq_api_key_here`
- `GOOGLE_CLIENT_ID=...`

## 4) Notes on speeding question generation

- The service already batches question generation and runs batches in parallel. If you still see slowness: increase `MAX_QUESTIONS_PER_BATCH` and `max_workers` in `backend/app/services/ai_service.py`, but watch LLM rate limits and quotas.

## 5) Next steps I can do for you

- Create CI that builds and deploys to Vercel on push.
- Add a DB migration workflow (`alembic`) for production schema changes.
