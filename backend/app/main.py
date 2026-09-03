from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app.routers import auth, exams, mock_tests, analytics, users
from app.utils.seed_data import seed_database
from app.models import user, exam, question, test_attempt, bookmark

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    Base.metadata.create_all(bind=engine)
    # Seed data if empty
    db = SessionLocal()
    try:
        from app.models.exam import ExamCategory
        if db.query(ExamCategory).count() == 0:
            seed_database(db)
    finally:
        db.close()
        
    import asyncio
    from app.services.generation_worker import generation_worker_loop
    worker_task = asyncio.create_task(generation_worker_loop())
    
    yield
    
    worker_task.cancel()
    try:
        await worker_task
    except asyncio.CancelledError:
        pass

app = FastAPI(
    title="MockBees API",
    description="AI-Powered Competitive Exam Mock Test Platform",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1|.*\.onrender\.com)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(exams.router, prefix="/api/exams", tags=["Exams"])
app.include_router(mock_tests.router, prefix="/api/mock-tests", tags=["Mock Tests"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "MockBees API"}

import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Serve static files from the 'static' directory if it exists (for Docker deployments)
if os.path.isdir("static"):
    app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")
    
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if full_path.startswith("api/"):
            return {"error": "Not found"}
        
        file_path = os.path.join("static", full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
            
        return FileResponse("static/index.html")
