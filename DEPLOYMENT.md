# Deploying MockBees to Render (and local Postgres setup)

This document explains how to deploy the `mockbees` project to Render (frontend + Python backend) and how to run a local Postgres-based development stack using Docker Compose.

## 1) Render deployment (recommended for production frontend + backend)

Steps:

1. Push your repo to GitHub.
2. Connect your GitHub repository to Render (https://render.com).
3. Create services from `render.yaml`:
   - **Backend Service** (Python/FastAPI):
     - Build command: `cd backend && pip install -r requirements.txt`
     - Start command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     - Plan: Starter (or higher as needed)
   - **Frontend Service** (Static):
     - Build command: `cd frontend && npm install && npm run build`
     - Publish path: `frontend/dist`
     - Plan: Starter

4. Add Environment Variables in Render Dashboard:
   - `DATABASE_URL` — e.g. `postgresql://user:pass@host:5432/dbname` (use a managed Postgres)
   - `SECRET_KEY` — a long random string
   - `GROQ_API_KEY` — required for AI question generation
   - `GOOGLE_CLIENT_ID` — optional
   - `VITE_API_URL` — set to your backend service URL (e.g., `https://mockbees-backend.onrender.com/api`)

5. Render will automatically build and deploy both services using the `render.yaml` configuration.

Notes:
- Use a managed Postgres database (Render provides this) for production — do NOT use SQLite.
- Make sure your `GROQ_API_KEY` account has sufficient quota for generation.
- The frontend service will connect to the backend using the `VITE_API_URL` environment variable.

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
